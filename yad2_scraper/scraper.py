import logging
import httpx
import time
from typing import Optional, Dict, Any, Callable, Union, Type, TypeVar

from yad2_scraper.category import Yad2Category
from yad2_scraper.query import QueryFilters
from yad2_scraper.utils import get_random_user_agent
from yad2_scraper.exceptions import AntiBotDetectedError, UnexpectedContentError, MaxRequestAttemptsExceededError
from yad2_scraper.constants import (
    DEFAULT_REQUEST_HEADERS,
    ALLOW_REQUEST_REDIRECTS,
    VERIFY_REQUEST_SSL,
    ANTIBOT_CONTENT_IDENTIFIER,
    YAD2_GET_CONTENT_IDENTIFIER
)

Category = TypeVar("Category", bound=Yad2Category)
WaitStrategy = Callable[[int], Optional[float]]
QueryParamTypes = Union[QueryFilters, Dict[str, Any]]

logger = logging.getLogger(__name__)


class Yad2Scraper:
    def __init__(
            self,
            client: Optional[httpx.Client] = None,
            request_defaults: Optional[Dict[str, Any]] = None,
            randomize_user_agent: bool = False,
            wait_strategy: Optional[WaitStrategy] = None,
            max_attempts: int = 1
    ):
        self.client = client or httpx.Client(
            headers=DEFAULT_REQUEST_HEADERS,
            follow_redirects=ALLOW_REQUEST_REDIRECTS,
            verify=VERIFY_REQUEST_SSL
        )
        self.request_defaults = request_defaults or {}
        self.randomize_user_agent = randomize_user_agent
        self.wait_strategy = wait_strategy
        self.max_attempts = max_attempts

        logger.debug(f"Scraper initialized with client: {self.client}")

    def set_user_agent(self, user_agent: str) -> None:
        self.client.headers["User-Agent"] = user_agent
        logger.debug(f"User-Agent client header set to: '{user_agent}'")

    def set_no_script(self, no_script: bool) -> None:
        value = "1" if no_script else "0"
        self.client.cookies.set("noscript", value)
        logger.debug(f"NoScript (noscript) client cookie set to: '{value}'")

    def fetch_category(
            self,
            url: str,
            params: Optional[QueryParamTypes] = None,
            category_type: Type[Category] = Yad2Category
    ) -> Category:
        logger.debug(f"Fetching category from URL: '{url}'")
        response = self.get(url, params)
        logger.debug(f"Category fetched successfully from URL: '{url}'")
        return category_type.from_html_io(response)

    def get(self, url: str, params: Optional[QueryParamTypes] = None) -> httpx.Response:
        return self.request("GET", url, params=params)

    def request(self, method: str, url: str, params: Optional[QueryParamTypes] = None) -> httpx.Response:
        if not isinstance(self.max_attempts, int):
            raise TypeError(f"Max attempts must be of type 'int', but got {type(self.max_attempts)}.")

        if self.max_attempts <= 0:
            raise ValueError(f"Max attempts must be a positive integer, but got {self.max_attempts}.")

        request_options = self._prepare_request_options(params=params)
        error_list = []

        for attempt in range(1, self.max_attempts + 1):
            try:
                return self._send_request(method, url, request_options, attempt)
            except Exception as error:
                logger.error(f"{method} request to '{url}' failed {self._format_attempt_info(attempt)}: {error}")
                error_list.append(error)

        if self.max_attempts == 1:
            raise error_list[0]  # Only one error exists - raise it

        max_attempts_error = MaxRequestAttemptsExceededError(method, url, self.max_attempts, error_list)
        logger.error(str(max_attempts_error))
        raise max_attempts_error from error_list[-1]

    def close(self) -> None:
        logger.debug("Closing scraper client")
        self.client.close()
        logger.info("Scraper client closed")

    def _send_request(self, method: str, url: str, request_options: Dict[str, Any], attempt: int) -> httpx.Response:
        if self.randomize_user_agent:
            self._set_random_user_agent_in_request_options(request_options)

        if self.wait_strategy:
            self._wait_before_request_attempt(attempt)

        logger.info(f"Sending {method} request to URL: '{url}' {self._format_attempt_info(attempt)}")
        response = self.client.request(method, url, **request_options)
        logger.debug(f"Received response {response.status_code} from '{url}' {self._format_attempt_info(attempt)}")
        self._validate_response(response)

        return response

    def _prepare_request_options(self, params: Optional[QueryParamTypes] = None) -> Dict[str, Any]:
        logger.debug("Preparing request options from defaults")
        request_options = self.request_defaults.copy()

        if params:
            request_options.setdefault("params", {}).update(params)
            logger.debug(f"Updated request options with query params: {params}")

        return request_options

    @staticmethod
    def _set_random_user_agent_in_request_options(request_options: Dict[str, str]):
        user_agent = get_random_user_agent()
        request_options.setdefault("headers", {})["User-Agent"] = user_agent
        logger.debug(f"Updated request options with random User-Agent header: '{user_agent}'")

    def _wait_before_request_attempt(self, attempt: int):
        wait_time = self.wait_strategy(attempt)
        if not wait_time:
            return

        logger.debug(f"Waiting {wait_time:.2f} seconds before request {self._format_attempt_info(attempt)}")
        time.sleep(wait_time)

    @staticmethod
    def _validate_response(response: httpx.Response):
        response.raise_for_status()

        if ANTIBOT_CONTENT_IDENTIFIER in response.content:
            raise AntiBotDetectedError(
                f"The response contains Anti-Bot content",
                request=response.request,
                response=response
            )
        if response.request.method == "GET" and YAD2_GET_CONTENT_IDENTIFIER not in response.content:
            raise UnexpectedContentError(
                "The GET response does not contain yad2 related content",
                request=response.request,
                response=response
            )

        logger.debug("Response validation succeeded")

    def _format_attempt_info(self, attempt: int) -> str:
        return f"(attempt {attempt}/{self.max_attempts})"

    def __enter__(self):
        logger.debug("Entering scraper context")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Exiting scraper context")
        self.close()

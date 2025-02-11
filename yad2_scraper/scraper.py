import logging
import httpx
import time
import random
from typing import Optional, Dict, Any, Callable, Union, Type, TypeVar

from yad2_scraper.category import Yad2Category
from yad2_scraper.query import QueryFilters
from yad2_scraper.utils import get_random_user_agent
from yad2_scraper.exceptions import AntiBotDetectedError, UnexpectedContentError, MaxRequestRetriesExceededError
from yad2_scraper.constants import (
    DEFAULT_REQUEST_HEADERS,
    ALLOW_REQUEST_REDIRECTS,
    VERIFY_REQUEST_SSL,
    ANTIBOT_CONTENT_IDENTIFIER,
    YAD2_CONTENT_IDENTIFIER
)

Category = TypeVar("Category", bound=Yad2Category)
DelayStrategy = Callable[[], None]
QueryParamTypes = Union[QueryFilters, Dict[str, Any]]

logger = logging.getLogger(__name__)


class Yad2Scraper:
    def __init__(
            self,
            client: Optional[httpx.Client] = None,
            request_defaults: Optional[Dict[str, Any]] = None,
            randomize_user_agent: bool = False,
            delay_strategy: Optional[DelayStrategy] = None,
            max_retries: int = 0
    ):
        self.client = client or httpx.Client(
            headers=DEFAULT_REQUEST_HEADERS,
            follow_redirects=ALLOW_REQUEST_REDIRECTS,
            verify=VERIFY_REQUEST_SSL
        )
        self.request_defaults = request_defaults or {}
        self.randomize_user_agent = randomize_user_agent
        self.delay_strategy = delay_strategy
        self.max_retries = max_retries

        logger.debug(f"Scraper initialized with client: {self.client}")

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
        request_options = self._prepare_request_options(params=params)

        try:
            return self._send_request(method, url, request_options)
        except Exception as error:
            return self._handle_request_error(method, url, request_options, error)

    def set_user_agent(self, user_agent: str) -> None:
        self.client.headers["User-Agent"] = user_agent
        logger.debug(f"User-Agent client header set to: '{user_agent}'")

    def set_no_script(self, no_script: bool) -> None:
        value = "1" if no_script else "0"
        self.client.cookies.set("noscript", value)
        logger.debug(f"noscript client cookie set to: '{value}'")

    def close(self) -> None:
        logger.debug("Closing scraper client")
        self.client.close()
        logger.info("Scraper client closed")

    def _send_request(self, method: str, url: str, request_options: Dict[str, Any]) -> httpx.Response:
        if self.randomize_user_agent:
            self._set_random_user_agent(request_options)

        if self.delay_strategy:
            self._apply_delay_strategy()

        logger.info(f"Making {method} request to URL: '{url}'")
        response = self.client.request(method, url, **request_options)
        logger.debug(f"Received response with status code: {response.status_code}")
        self._validate_response(response)

        return response

    def _handle_request_error(
            self,
            method: str,
            url: str,
            request_options: Dict[str, Any],
            error: Exception
    ) -> httpx.Response:
        logger.error(f"{method} request to '{url}' failed: {error}")

        if self.max_retries == 0:
            raise error

        return self._retry_request(method, url, request_options)

    def _retry_request(self, method: str, url: str, request_options: Dict[str, Any]) -> httpx.Response:
        logger.info(f"Retrying {method} request to '{url}' (max retries: {self.max_retries})")

        errors = []

        for retry_attempt in range(1, self.max_retries + 1):
            try:
                logger.debug(f"Retry attempt {retry_attempt}/{self.max_retries}")
                return self._send_request(method, url, request_options)
            except Exception as error:
                logger.warning(f"Retry attempt {retry_attempt} failed: {error}")
                errors.append(error)

        error_to_raise = MaxRequestRetriesExceededError(method, url, self.max_retries, errors)
        logger.error(str(error_to_raise))
        raise error_to_raise from errors[-1]

    def _prepare_request_options(self, params: Optional[QueryParamTypes] = None) -> Dict[str, Any]:
        logger.debug("Preparing request options from defaults")
        request_options = self.request_defaults.copy()

        if params:
            request_options.setdefault("params", {}).update(params)
            logger.debug(f"Updated request options with query params: {params}")

        return request_options

    def _apply_delay_strategy(self):
        logger.debug(f"Applying request delay strategy")
        self.delay_strategy()

    @staticmethod
    def _set_random_user_agent(request_options: Dict[str, str]):
        user_agent = get_random_user_agent()
        request_options.setdefault("headers", {})["User-Agent"] = user_agent
        logger.debug(f"Updated request options with random User-Agent header: '{user_agent}'")

    @staticmethod
    def _validate_response(response: httpx.Response):
        response.raise_for_status()

        if ANTIBOT_CONTENT_IDENTIFIER in response.content:
            raise AntiBotDetectedError(
                f"The response contains Anti-Bot content",
                request=response.request,
                response=response
            )
        if YAD2_CONTENT_IDENTIFIER not in response.content:
            raise UnexpectedContentError(
                "The response does not contain yad2 related content",
                request=response.request,
                response=response
            )

        logger.debug("Response validation succeeded")

    def __enter__(self):
        logger.debug("Entering scraper context")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Exiting scraper context")
        self.close()

import logging
import httpx
import time
from fake_useragent import FakeUserAgent
from typing import Optional, Dict, Any, Callable, Union, Type, TypeVar

from yad2_scraper.category import Yad2Category
from yad2_scraper.query import QueryFilters
from yad2_scraper.exceptions import AntiBotDetectedError, UnexpectedContentError, MaxRequestAttemptsExceededError
from yad2_scraper.constants import (
    DEFAULT_REQUEST_HEADERS,
    ALLOW_REQUEST_REDIRECTS,
    VERIFY_REQUEST_SSL,
    ANTIBOT_CONTENT_IDENTIFIER,
    PAGE_CONTENT_IDENTIFIER
)

Category = TypeVar("Category", bound=Yad2Category)
WaitStrategy = Callable[[int], Optional[float]]
QueryParamTypes = Union[QueryFilters, Dict[str, Any]]

fua = FakeUserAgent()
logger = logging.getLogger(__name__)


class Yad2Scraper:
    """A scraper for fetching data from the Yad2 website, with robust features"""

    def __init__(
            self,
            client: Optional[httpx.Client] = None,
            request_defaults: Optional[Dict[str, Any]] = None,
            randomize_user_agent: bool = True,
            wait_strategy: Optional[WaitStrategy] = None,
            max_request_attempts: int = 1
    ):
        """
        Initializes the Yad2Scraper with provided parameters.

        Args:
            client (Optional[httpx.Client]): An optional custom HTTP client. If not provided, a default client is used.
            request_defaults (Optional[Dict[str, Any]]): Default parameters for requests such as headers, params, etc.
            randomize_user_agent (bool): If True, a random User-Agent will be set for each request. Defaults to True.
            wait_strategy (Optional[WaitStrategy]): A function to determine the wait time between requests.
            max_request_attempts (int): The maximum number of retry attempts for failed requests. Defaults to 1.
        """
        self.client = client or httpx.Client(
            headers=DEFAULT_REQUEST_HEADERS,
            follow_redirects=ALLOW_REQUEST_REDIRECTS,
            verify=VERIFY_REQUEST_SSL
        )
        self.request_defaults = request_defaults or {}
        self.randomize_user_agent = randomize_user_agent
        self.wait_strategy = wait_strategy
        self.max_request_attempts = max_request_attempts
        self._request_count = 0

        logger.debug(f"Scraper initialized with client: {self.client}")

    @property
    def request_count(self) -> int:
        """Returns the number of requests made by the scraper so far."""
        return self._request_count

    def set_user_agent(self, user_agent: str) -> None:
        """
        Sets the User-Agent header for requests.

        Args:
            user_agent (str): The User-Agent string to be used in HTTP requests.
        """
        self.client.headers["User-Agent"] = user_agent
        logger.debug(f"User-Agent client header set to: '{user_agent}'")

    def set_no_script(self, no_script: bool) -> None:
        """
        Sets the "noscript" cookie in the client's cookies to control JavaScript content.

        Args:
            no_script (bool): If True, the "noscript" cookie is set to "1". If False, it's set to "0".
        """
        value = "1" if no_script else "0"
        self.client.cookies.set("noscript", value)
        logger.debug(f"NoScript (noscript) client cookie set to: '{value}'")

    def fetch_category(
            self,
            url: str,
            category_type: Type[Category],
            params: Optional[QueryParamTypes] = None
    ) -> Category:
        """
        Fetches and returns a category page from a given URL.

        Args:
            url (str): The URL of the category page.
            category_type (Type[Category]): The class type of the category to be fetched.
            params (Optional[QueryParamTypes]): Query parameters to be included in the request.

        Returns:
            Category: The fetched category, parsed from HTML.
        """
        logger.debug(f"Fetching category from URL: '{url}'")
        response = self.get(url, params)
        logger.debug(f"Category fetched successfully from URL: '{url}'")
        return category_type.from_html_io(response)

    def get(self, url: str, params: Optional[QueryParamTypes] = None) -> httpx.Response:
        """Sends a GET request to the specified URL."""
        return self.request("GET", url, params=params)

    def request(self, method: str, url: str, params: Optional[QueryParamTypes] = None) -> httpx.Response:
        """
        Sends an HTTP request with multiple attempts logic.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").
            url (str): The URL to send the request to.
            params (Optional[QueryParamTypes]): Query parameters to be included in the request.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            MaxRequestAttemptsExceededError: If the request exceeds the maximum number of attempts.
        """
        if not isinstance(self.max_request_attempts, int):
            raise TypeError(f"max_request_attempts must be of type 'int', but got {type(self.max_request_attempts)}")

        if self.max_request_attempts <= 0:
            raise ValueError(f"max_request_attempts must be a positive integer, but got {self.max_request_attempts}")

        request_options = self._prepare_request_options(params=params)
        error_list = []

        for attempt in range(1, self.max_request_attempts + 1):
            try:
                return self._send_request(method, url, request_options, attempt)
            except Exception as error:
                logger.error(f"{method} request to '{url}' failed {self._format_attempt_info(attempt)}: {error}")
                error_list.append(error)

        if self.max_request_attempts == 1:
            raise error_list[0]  # only one error exists, raise it

        max_attempts_error = MaxRequestAttemptsExceededError(method, url, self.max_request_attempts, error_list)
        logger.error(str(max_attempts_error))
        raise max_attempts_error from error_list[-1]  # multiple errors exist, raise from the last one

    def close(self) -> None:
        """Closes the HTTP client and logs the closure."""
        logger.debug("Closing scraper client")
        self.client.close()
        logger.info("Scraper client closed")

    def _send_request(self, method: str, url: str, request_options: Dict[str, Any], attempt: int) -> httpx.Response:
        """
        Sends an HTTP request with the specified method to the given URL, applying all necessary actions.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST').
            url (str): The target URL for the request.
            request_options (Dict[str, Any]): Additional request options, including headers and parameters.
            attempt (int): The current attempt number for the request.

        Returns:
            httpx.Response: The HTTP response object received from the server.

        Raises:
            AntiBotDetectedError: If the response contains Anti-Bot content.
            UnexpectedContentError: If a GET request does not contain expected content.
        """
        if self.randomize_user_agent:
            self._set_random_user_agent(request_options)

        if self.wait_strategy:
            self._apply_wait_strategy(attempt)

        logger.info(f"Sending {method} request to URL: '{url}' {self._format_attempt_info(attempt)}")
        response = self.client.request(method, url, **request_options)
        self._request_count += 1
        logger.debug(f"Received response {response.status_code} from '{url}' {self._format_attempt_info(attempt)}")
        self._validate_response(response)

        return response

    def _prepare_request_options(self, params: Optional[QueryParamTypes] = None) -> Dict[str, Any]:
        """
        Prepares the request options to be passed to the HTTP client's request method, based on the default options.

        Args:
            params (Optional[QueryParamTypes]): Optional query parameters to include in the request.

        Returns:
            Dict[str, Any]: A dictionary of the request options, including headers and query parameters.
        """
        logger.debug("Preparing request options from defaults")
        request_options = self.request_defaults.copy()

        if params:
            request_options.setdefault("params", {}).update(params)
            logger.debug(f"Updated request options with query params: {params}")

        return request_options

    @staticmethod
    def _set_random_user_agent(request_options: Dict[str, str]):
        """
        Sets a random User-Agent header in the request options.

        Args:
            request_options (Dict[str, str]): The request options to update with the random User-Agent.
        """
        user_agent = fua.random
        request_options.setdefault("headers", {})["User-Agent"] = user_agent
        logger.debug(f"Updated request options with random User-Agent header: '{user_agent}'")

    def _apply_wait_strategy(self, attempt: int):
        """
        Applies a wait time before making a request based on the wait strategy for the given attempt.

        Args:
            attempt (int): The current attempt number to calculate the wait time.
        """
        wait_time = self.wait_strategy(attempt)
        if not wait_time:
            return

        logger.debug(f"Waiting {wait_time:.2f} seconds before request {self._format_attempt_info(attempt)}")
        time.sleep(wait_time)

    @staticmethod
    def _validate_response(response: httpx.Response):
        """
        Validates the response to ensure it is successful.

        Args:
            response (httpx.Response): The HTTP response object to validate.

        Raises:
            httpx.HTTPStatusError: If a status error occurred.
            AntiBotDetectedError: If the response contains Anti-Bot content.
            UnexpectedContentError: If a GET response does not contain expected content.
        """
        response.raise_for_status()

        if ANTIBOT_CONTENT_IDENTIFIER in response.content:
            raise AntiBotDetectedError(
                f"The response contains Anti-Bot content",
                request=response.request,
                response=response
            )
        if response.request.method == "GET" and PAGE_CONTENT_IDENTIFIER not in response.content:
            raise UnexpectedContentError(
                "The GET response does not contain yad2 related content",
                request=response.request,
                response=response
            )

        logger.debug("Response validation succeeded")

    def _format_attempt_info(self, attempt: int) -> str:
        """
        Formats a string representing the current attempt number and total attempt count.

        Args:
            attempt (int): The current attempt number.

        Returns:
            str: A formatted string representing the attempt info, e.g., "(attempt 1/5)".
        """
        return f"(attempt {attempt}/{self.max_request_attempts})"

    def __enter__(self):
        """
        Prepares the scraper to be used in a `with` statement, allowing for resource management.

        Returns:
            Yad2Scraper: The scraper instance to be used within the `with` block.
        """
        logger.debug("Entering scraper context")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Cleans up resources and closes the scraper client when exiting the `with` statement.

        Args:
            exc_type: The exception type (if any).
            exc_val: The exception value (if any).
            exc_tb: The traceback object (if any).
        """
        logger.debug("Exiting scraper context")
        self.close()

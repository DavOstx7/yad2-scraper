import logging
import httpx
import time
import random
from typing import Optional, Dict, Any, Tuple, Union, Type, TypeVar

from yad2_scraper.category import Yad2Category
from yad2_scraper.query import QueryFilters
from yad2_scraper.utils import get_random_user_agent, validate_http_response
from yad2_scraper.constants import (
    DEFAULT_REQUEST_HEADERS,
    ALLOW_REQUEST_REDIRECTS,
    VERIFY_REQUEST_SSL
)

Category = TypeVar("Category", bound=Yad2Category)
DelayRange = Tuple[float, float]
QueryParams = Union[QueryFilters, Dict[str, Any]]

logger = logging.getLogger(__name__)


class Yad2Scraper:
    def __init__(
            self,
            session: Optional[httpx.Client] = None,
            request_kwargs: Dict[str, Any] = None,
            randomize_user_agent: bool = False,
            requests_delay_range: Optional[DelayRange] = None,
    ):
        self.session = session or httpx.Client(
            headers=DEFAULT_REQUEST_HEADERS,
            follow_redirects=ALLOW_REQUEST_REDIRECTS,
            verify=VERIFY_REQUEST_SSL
        )
        self.request_kwargs = request_kwargs or {}
        self.randomize_user_agent = randomize_user_agent
        self.requests_delay_range = requests_delay_range

        logger.debug(f"Initialized with session {self.session} and request kwargs: {self.request_kwargs}")

    def set_user_agent(self, user_agent: str):
        self.session.headers["User-Agent"] = user_agent
        logger.debug(f"User-Agent session header set to: '{user_agent}'")

    def set_no_script(self, no_script: bool):
        value = "1" if no_script else "0"  # str(int(no_script))
        self.session.cookies.set("noscript", value)
        logger.debug(f"NoScript session cookie set to: '{value}'")

    def fetch_category(
            self,
            url: str,
            query_params: Optional[QueryParams] = None,
            category_type: Type[Category] = Yad2Category
    ) -> Category:
        logger.debug(f"Fetching category from URL: '{url}'")
        response = self.get(url, query_params)
        logger.debug(f"Category fetched successfully from URL: '{url}'")
        return category_type.from_html_io(response)

    def get(self, url: str, query_params: Optional[QueryParams] = None) -> httpx.Response:
        return self.request("GET", url, query_params=query_params)

    def request(self, method: str, url: str, query_params: Optional[QueryParams] = None) -> httpx.Response:
        request_kwargs = self._prepare_request_kwargs(query_params=query_params)

        if self.requests_delay_range:
            self._apply_request_delay()

        try:
            logger.info(f"Making {method} request to URL: '{url}'")  # request kwargs not logged - may be sensitive
            response = self.session.request(method, url, **request_kwargs)
            logger.debug(f"Received response with status code: {response.status_code}")

            validate_http_response(response)
            logger.debug("Response validation succeeded")
        except Exception as error:
            logger.error(f"Request to '{url}' failed: {error}")
            raise error

        return response

    def _prepare_request_kwargs(self, query_params: Optional[QueryParams] = None) -> Dict[str, Any]:
        logger.debug("Preparing request kwargs from defaults")
        request_kwargs = self.request_kwargs.copy()

        if query_params:
            request_kwargs.setdefault("params", {}).update(query_params)
            logger.debug(f"Updated request kwargs with query params: {query_params}")

        if self.randomize_user_agent:
            random_user_agent = get_random_user_agent()
            request_kwargs.setdefault("headers", {})["User-Agent"] = random_user_agent
            logger.debug(f"Updated request kwargs with random 'User-Agent' header: '{random_user_agent}'")

        return request_kwargs

    def _apply_request_delay(self):
        delay = random.uniform(*self.requests_delay_range)
        logger.debug(f"Applying request delay of {delay:.2f} seconds")
        time.sleep(delay)

    def close(self):
        logger.debug("Closing scraper session")
        self.session.close()
        logger.info("Scraper session closed")

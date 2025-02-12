import pytest
import respx
import httpx
import random
import time
from unittest.mock import patch

from yad2_scraper.scraper import Yad2Scraper, Yad2Category
from yad2_scraper.exceptions import AntiBotDetectedError, MaxRequestRetriesExceededError, UnexpectedContentError
from yad2_scraper.constants import ANTIBOT_CONTENT_IDENTIFIER, YAD2_CONTENT_IDENTIFIER


@pytest.fixture
def scraper():
    with httpx.Client() as client:
        yield Yad2Scraper(client=client)


@pytest.fixture
def mock_http():
    with respx.mock as mock:
        yield mock


def _create_success_response() -> httpx.Response:
    return httpx.Response(status_code=200, content=YAD2_CONTENT_IDENTIFIER)


def _assert_success_response(response: httpx.Response):
    assert response.status_code == 200
    assert response.content == YAD2_CONTENT_IDENTIFIER


def test_get_request(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).return_value = _create_success_response()

    response = scraper.get(url)

    _assert_success_response(response)


def test_get_request_with_params(scraper, mock_http):
    url = "https://example.com"
    params = {"key": "value"}
    mock_http.get(url, params=params).return_value = _create_success_response()

    response = scraper.get(url, params=params)

    _assert_success_response(response)
    assert b"key=value" in response.request.url.query


def test_get_request_with_random_user_agent(scraper, mock_http):
    url = "https://example.com"
    scraper.randomize_user_agent = True

    with patch("yad2_scraper.scraper.get_random_user_agent", return_value="RandomUserAgent/1.0"):
        mock_http.get(url).return_value = _create_success_response()
        response = scraper.get(url)

    _assert_success_response(response)
    assert response.request.headers["User-Agent"] == "RandomUserAgent/1.0"


def test_get_request_with_delay(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).return_value = _create_success_response()


    with patch("random.uniform", return_value=1.5), patch("time.sleep") as mock_sleep:
        scraper.delay_strategy = lambda: random.uniform(1, 3)
        response = scraper.get(url)
        mock_sleep.assert_called_once_with(1.5)

    _assert_success_response(response)

def test_get_request_with_retry(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).side_effect = [httpx.RequestError("Request failed"), _create_success_response()]
    scraper.max_retries = 3

    response = scraper.get(url)

    _assert_success_response(response)


def test_get_request_http_status_error(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).return_value = httpx.Response(status_code=404, content=b"Not Found")

    with pytest.raises(httpx.HTTPStatusError):
        scraper.get(url)


def test_get_request_anti_bot_detected_error(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).return_value = httpx.Response(status_code=200, content=ANTIBOT_CONTENT_IDENTIFIER)

    with pytest.raises(AntiBotDetectedError) as error:
        scraper.get(url)
        assert isinstance(error, httpx.HTTPStatusError)

def test_get_request_unexpected_content_error(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).return_value = httpx.Response(status_code=200, content=b"Invalid Content")

    with pytest.raises(UnexpectedContentError) as error:
        scraper.get(url)
        assert isinstance(error, httpx.HTTPStatusError)

def test_get_request_max_retries_exceeded_error(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).side_effect = httpx.RequestError("Request failed")

    scraper.max_retries = 3

    with pytest.raises(MaxRequestRetriesExceededError):
        scraper.get(url)


def test_fetch_category(scraper, mock_http):
    url = "http://example.com"
    mock_http.get(url).mock(return_value=_create_success_response())

    class MockYad2Category(Yad2Category):
        @classmethod
        def from_html_io(cls, response):
            return "parsed_category"

    result = scraper.fetch_category(url, category_type=MockYad2Category)
    assert result == "parsed_category"


def test_client_user_agent(scraper):
    user_agent = "test_agent"
    scraper.set_user_agent(user_agent)
    assert scraper.client.headers["User-Agent"] == user_agent


def test_client_no_script(scraper):
    scraper.set_no_script(True)
    assert scraper.client.cookies["noscript"] == "1"
    scraper.set_no_script(False)
    assert scraper.client.cookies["noscript"] == "0"


def test_client(scraper):
    scraper.close()
    assert scraper.client.is_closed


def test_context_manager(scraper):
    with scraper:
        pass

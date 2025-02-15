import pytest
import respx
import httpx
import random
from unittest.mock import patch

from yad2_scraper.scraper import Yad2Scraper, Yad2Category
from yad2_scraper.exceptions import AntiBotDetectedError, MaxRequestAttemptsExceededError, UnexpectedContentError
from yad2_scraper.constants import ANTIBOT_CONTENT_IDENTIFIER, PAGE_CONTENT_IDENTIFIER


@pytest.fixture
def scraper():
    with httpx.Client() as client:
        yield Yad2Scraper(client=client)


@pytest.fixture
def mock_http():
    with respx.mock as mock:
        yield mock


def _create_success_response() -> httpx.Response:
    return httpx.Response(status_code=200, content=PAGE_CONTENT_IDENTIFIER)


def _assert_success_response(response: httpx.Response):
    assert response.status_code == 200
    assert response.content == PAGE_CONTENT_IDENTIFIER


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
    mock_http.get(url).return_value = _create_success_response()
    scraper.set_user_agent("RandomUserAgent/1.0")
    scraper.randomize_user_agent = True

    response = scraper.get(url)

    _assert_success_response(response)
    assert response.request.headers["User-Agent"] != "RandomUserAgent/1.0"


def test_get_request_with_wait_strategy(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).return_value = _create_success_response()

    with patch("random.uniform", return_value=1.5), patch("time.sleep") as mock_sleep:
        scraper.wait_strategy = lambda attempt: random.uniform(1, 3 * attempt)
        response = scraper.get(url)
        mock_sleep.assert_called_once_with(1.5)

    _assert_success_response(response)


def test_get_request_with_multiple_attempts(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).side_effect = [
        httpx.RequestError("Request failed"),
        httpx.RequestError("Request failed"),
        _create_success_response()
    ]
    scraper.max_request_attempts = 3

    response = scraper.get(url)

    _assert_success_response(response)

def test_get_request_increment_counter(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).return_value = _create_success_response()
    request_count = random.randint(1, 3)

    for _ in range(request_count):
        response = scraper.get(url)
        _assert_success_response(response)

    assert scraper.request_count == request_count


def test_get_request_http_status_error(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).return_value = httpx.Response(status_code=404, content=b"Not Found")

    with pytest.raises(httpx.HTTPStatusError):
        scraper.get(url)


def test_get_request_anti_bot_detected_error(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).return_value = httpx.Response(status_code=200, content=ANTIBOT_CONTENT_IDENTIFIER)

    with pytest.raises(AntiBotDetectedError):
        scraper.get(url)


def test_get_request_unexpected_content_error(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).return_value = httpx.Response(status_code=200, content=b"Invalid Content")

    with pytest.raises(UnexpectedContentError):
        scraper.get(url)


def test_get_request_max_attempts_type_error(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).side_effect = httpx.RequestError("Request failed")

    scraper.max_request_attempts = "invalid_type"
    with pytest.raises(TypeError):
        scraper.get(url)


def test_get_request_max_attempts_value_error(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).side_effect = httpx.RequestError("Request failed")

    scraper.max_request_attempts = -3
    with pytest.raises(ValueError):
        scraper.get(url)


def test_get_request_max_attempts_exceeded_error(scraper, mock_http):
    url = "https://example.com"
    mock_http.get(url).side_effect = httpx.RequestError("Request failed")
    scraper.max_request_attempts = 3

    with pytest.raises(MaxRequestAttemptsExceededError):
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


def test_set_user_agent(scraper):
    user_agent = "test_agent"
    scraper.set_user_agent(user_agent)
    assert scraper.client.headers["User-Agent"] == user_agent


def test_set_no_script(scraper):
    scraper.set_no_script(True)
    assert scraper.client.cookies["noscript"] == "1"
    scraper.set_no_script(False)
    assert scraper.client.cookies["noscript"] == "0"


def test_close(scraper):
    scraper.close()
    assert scraper.client.is_closed


def test_context_manager(scraper):
    with scraper:
        pass

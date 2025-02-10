import pytest
import httpx
from unittest.mock import patch, MagicMock

from yad2_scraper.scraper import Yad2Scraper, Yad2Category


# Initialization Tests
def test_initialization_defaults():
    scraper = Yad2Scraper()
    assert isinstance(scraper.session, httpx.Client)
    assert scraper.request_defaults == {}
    assert scraper.randomize_user_agent is False
    assert scraper.random_delay_range is None


def test_initialization_custom():
    session_mock = MagicMock()
    scraper = Yad2Scraper(
        session=session_mock,
        request_defaults={"timeout": 10},
        randomize_user_agent=True,
        random_delay_range=(1, 3)
    )
    assert scraper.session == session_mock
    assert scraper.request_defaults == {"timeout": 10}
    assert scraper.randomize_user_agent is True
    assert scraper.random_delay_range == (1, 3)


# Header & Cookie Tests
def test_set_user_agent(scraper):
    user_agent = "test_agent"
    scraper.set_user_agent(user_agent)
    assert scraper.session.headers["User-Agent"] == user_agent


def test_set_no_script(scraper):
    scraper.set_no_script(True)
    assert scraper.session.cookies["noscript"] == "1"
    scraper.set_no_script(False)
    assert scraper.session.cookies["noscript"] == "0"


# HTTP Request Tests
def test_request(scraper, mock_http):
    url = "http://example.com"
    mock_http.get(url).mock(return_value=httpx.Response(200, content=b"success"))

    response = scraper.request("GET", url)

    assert response.status_code == 200
    assert response.content == b"success"


def test_request_applies_random_delay(scraper, mock_http):
    url = "http://example.com"
    scraper.random_delay_range = (1, 2)
    mock_http.get(url).mock(return_value=httpx.Response(200, content=b"test content"))

    with patch.object(scraper, "apply_random_delay") as mock_apply_random_delay:
        response = scraper.request("GET", url)
        mock_apply_random_delay.assert_called_once()
        assert response.status_code == 200


def test_request_validates_response(scraper, mock_http):
    url = "http://example.com"
    mock_http.get(url).mock(return_value=httpx.Response(500, content=b"error"))

    with patch("yad2_scraper.scraper.validate_http_response") as mock_validate_http_response:
        response = scraper.request("GET", url)
        mock_validate_http_response.assert_called_once_with(response)


def test_request_timeout(scraper, mock_http):
    url = "http://example.com"
    mock_http.get(url).mock(side_effect=httpx.TimeoutException("Request timed out"))

    with pytest.raises(httpx.TimeoutException, match="Request timed out"):
        scraper.request("GET", url)


def test_request_uses_default_request_options(scraper, mock_http):
    url = "http://example.com"
    scraper.request_defaults = {"headers": {"Authorization": "Bearer token"}}
    mock_http.get(url, headers={"Authorization": "Bearer token"}).mock(
        return_value=httpx.Response(200, content=b"success")
    )

    response = scraper.request("GET", url)

    assert response.status_code == 200


# Fetch Category Tests
def test_fetch_category(scraper, mock_http):
    url = "http://example.com"
    mock_http.get(url).mock(return_value=httpx.Response(200, content=b"page content"))

    class MockYad2Category(Yad2Category):
        @classmethod
        def from_html_io(cls, response):
            return "parsed_category"

    result = scraper.fetch_category(url, category_type=MockYad2Category)
    assert result == "parsed_category"


def test_fetch_category_with_query_params(scraper, mock_http):
    url = "http://example.com"
    query_params = {"key": "value"}
    mock_http.get(url, params=query_params).mock(return_value=httpx.Response(200, content=b"test"))

    class MockCategory(Yad2Category):
        @classmethod
        def from_html_io(cls, response):
            return "parsed_category_with_query"

    result = scraper.fetch_category(url, query_params=query_params, category_type=MockCategory)
    assert result == "parsed_category_with_query"


# Closing Tests
def test_close(scraper):
    scraper.close()
    assert scraper.session.is_closed


# Internal Helper Function Tests
def test_prepare_request_options(scraper):
    query_params = {"key": "value"}
    request_options = scraper.prepare_request_options(query_params=query_params)
    assert request_options["params"] == query_params


def test_prepare_request_options_with_query_params(scraper):
    query_params = {"key": "value"}
    request_options = scraper.prepare_request_options(query_params=query_params)

    assert "params" in request_options
    assert request_options["params"] == query_params


def test_prepare_request_options_merge_headers(scraper):
    scraper.request_defaults = {"headers": {"X-Test": "existing"}}
    request_options = scraper.prepare_request_options()

    assert "headers" in request_options
    assert request_options["headers"]["X-Test"] == "existing"


def test_prepare_request_options_preserve_existing_options(scraper):
    scraper.request_defaults = {"params": {"existing": "value"}}
    query_params = {"new": "param"}

    request_options = scraper.prepare_request_options(query_params=query_params)

    assert request_options["params"] == {"existing": "value", "new": "param"}


def test_prepare_request_options_random_user_agent(scraper):
    scraper.randomize_user_agent = True
    with patch("yad2_scraper.scraper.get_random_user_agent", return_value="random_agent"):
        request_options = scraper.prepare_request_options()
        assert request_options["headers"]["User-Agent"] == "random_agent"


def test_apply_random_delay(scraper):
    scraper.random_delay_range = (1, 2)
    with patch("random.uniform", return_value=1.5), patch("time.sleep") as mock_sleep:
        scraper.apply_random_delay()
        mock_sleep.assert_called_once_with(1.5)

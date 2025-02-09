import pytest
import httpx
from unittest.mock import patch, MagicMock

from yad2_scraper.scraper import Yad2Scraper, Yad2Category


# Initialization Tests
def test_initialization_defaults():
    scraper = Yad2Scraper()
    assert isinstance(scraper.session, httpx.Client)
    assert scraper.request_kwargs == {}
    assert scraper.randomize_user_agent is False
    assert scraper.requests_delay_range is None


def test_initialization_custom():
    session_mock = MagicMock()
    scraper = Yad2Scraper(
        session=session_mock,
        request_kwargs={"timeout": 10},
        randomize_user_agent=True,
        requests_delay_range=(1, 3)
    )
    assert scraper.session == session_mock
    assert scraper.request_kwargs == {"timeout": 10}
    assert scraper.randomize_user_agent is True
    assert scraper.requests_delay_range == (1, 3)


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


def test_request_with_delay(scraper, mock_http):
    url = "http://example.com"
    scraper.requests_delay_range = (1, 2)
    mock_http.get(url).mock(return_value=httpx.Response(200, content=b"test content"))

    with patch("time.sleep") as mock_sleep:
        response = scraper.request("GET", url)
        mock_sleep.assert_called_once()
        assert response.status_code == 200


def test_request_validation_failure(scraper, mock_http):
    url = "http://example.com"
    mock_http.get(url).mock(return_value=httpx.Response(500, content=b"error"))

    with pytest.raises(httpx.HTTPStatusError):
        scraper.request("GET", url)


def test_request_timeout(scraper, mock_http):
    url = "http://example.com"
    mock_http.get(url).mock(side_effect=httpx.TimeoutException("Request timed out"))

    with pytest.raises(httpx.TimeoutException, match="Request timed out"):
        scraper.request("GET", url)


def test_request_applies_request_kwargs(scraper, mock_http):
    url = "http://example.com"
    scraper.request_kwargs = {"headers": {"Authorization": "Bearer token"}}

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


def test_fetch_category_http_error(scraper, mock_http):
    url = "http://example.com"
    mock_http.get(url).mock(return_value=httpx.Response(500))

    with pytest.raises(httpx.HTTPStatusError):
        scraper.fetch_category(url, category_type=Yad2Category)


# Closing Tests
def test_close(scraper):
    scraper.close()
    assert scraper.session.is_closed


# Internal Helper Function Tests
def test_prepare_request_kwargs(scraper):
    query_params = {"key": "value"}
    request_kwargs = scraper._prepare_request_kwargs(query_params=query_params)
    assert request_kwargs["params"] == query_params


def test_prepare_request_kwargs_with_query_params(scraper):
    query_params = {"key": "value"}
    request_kwargs = scraper._prepare_request_kwargs(query_params=query_params)

    assert "params" in request_kwargs
    assert request_kwargs["params"] == query_params


def test_prepare_request_kwargs_merge_headers(scraper):
    scraper.request_kwargs = {"headers": {"X-Test": "existing"}}
    request_kwargs = scraper._prepare_request_kwargs()

    assert "headers" in request_kwargs
    assert request_kwargs["headers"]["X-Test"] == "existing"


def test_prepare_request_kwargs_preserve_existing_params(scraper):
    scraper.request_kwargs = {"params": {"existing": "value"}}
    query_params = {"new": "param"}

    request_kwargs = scraper._prepare_request_kwargs(query_params=query_params)

    assert request_kwargs["params"] == {"existing": "value", "new": "param"}


def test_prepare_request_kwargs_random_user_agent(scraper):
    scraper.randomize_user_agent = True
    with patch("yad2_scraper.scraper.get_random_user_agent", return_value="random_agent"):
        request_kwargs = scraper._prepare_request_kwargs()
        assert request_kwargs["headers"]["User-Agent"] == "random_agent"


def test_apply_request_delay(scraper):
    scraper.requests_delay_range = (1, 2)
    with patch("random.uniform", return_value=1.5), patch("time.sleep") as mock_sleep:
        scraper._apply_request_delay()
        mock_sleep.assert_called_once_with(1.5)

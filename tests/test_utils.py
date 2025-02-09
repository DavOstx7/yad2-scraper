import pytest
import httpx
from unittest.mock import MagicMock
from bs4 import BeautifulSoup

from yad2_scraper.utils import (
    join_url,
    get_parent_url,
    validate_http_response,
    find_html_tag_by_class_substring,
    find_all_html_tags_by_class_substring,
)
from yad2_scraper.exceptions import AntiBotDetectedError
from yad2_scraper.constants import ANTIBOT_CONTENT


@pytest.mark.parametrize(
    "url, path, expected",
    [
        ("http://example.com", "subpage", "http://example.com/subpage"),
        ("http://example.com/", "/subpage", "http://example.com/subpage"),
        ("http://example.com/", "subpage/", "http://example.com/subpage/"),
        ("http://example.com//", "//subpage", "http://example.com/subpage"),
    ],
)
def test_join_url(url, path, expected):
    assert join_url(url, path) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("http://example.com/page", "http://example.com"),
        ("http://example.com/page/", "http://example.com"),
        ("http://example.com/section/page", "http://example.com/section"),
        ("http://example.com", "http://example.com"),
    ],
)
def test_get_parent_url(url, expected):
    assert get_parent_url(url) == expected


def test_validate_http_response_success():
    response = MagicMock(spec=httpx.Response)
    response.status_code = 200
    response.content = b"valid content"

    validate_http_response(response)


def test_validate_http_response_raises_http_error():
    response = MagicMock(spec=httpx.Response)
    response.status_code = 500
    response.raise_for_status.side_effect = httpx.HTTPStatusError("Server error", request=None, response=response)

    with pytest.raises(httpx.HTTPStatusError, match="Server error"):
        validate_http_response(response)


def test_validate_http_response_antibot_detected():
    response = MagicMock(spec=httpx.Response)
    response.status_code = 200
    response.content = ANTIBOT_CONTENT if isinstance(ANTIBOT_CONTENT, bytes) else ANTIBOT_CONTENT.encode()

    with pytest.raises(AntiBotDetectedError, match="The response contains Anti-Bot content"):
        validate_http_response(response)


HTML_SAMPLE = """
<html>
    <body>
        <div class="some-class">Content 1</div>
        <div class="another-class">Content 2</div>
        <p class="test-class">Paragraph 1</p>
        <p class="test-class-other">Paragraph 2</p>
    </body>
</html>
"""


@pytest.fixture
def soup():
    return BeautifulSoup(HTML_SAMPLE, "html.parser")


def test_find_html_tag_by_class_substring(soup):
    tag = find_html_tag_by_class_substring(soup, "p", "test-class")
    assert tag is not None
    assert tag.name == "p"
    assert "test-class" in tag["class"]


def test_find_html_tag_by_class_substring_not_found(soup):
    tag = find_html_tag_by_class_substring(soup, "p", "nonexistent")
    assert tag is None


def test_find_all_html_tags_by_class_substring(soup):
    tags = find_all_html_tags_by_class_substring(soup, "p", "test-class")
    assert len(tags) == 2
    assert all(tag.name == "p" for tag in tags)
    assert any("test-class" in tag["class"] for tag in tags)
    assert any("test-class-other" in tag["class"] for tag in tags)


def test_find_all_html_tags_by_class_substring_no_match(soup):
    tags = find_all_html_tags_by_class_substring(soup, "p", "nonexistent")
    assert tags == []
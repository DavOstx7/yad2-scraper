import pytest
from bs4 import BeautifulSoup

from yad2_scraper.utils import (
    join_url,
    get_parent_url,
    find_html_tag_by_class_substring,
    find_all_html_tags_by_class_substring,
    safe_access
)


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


@pytest.mark.parametrize(
    "to_call, exceptions, expected",
    [
        (lambda: {"key": "value"}["key"], (KeyError,), "value"),
        (lambda: [0, 1, 2][0], (IndexError,), 0),
        (lambda: 1 / 1, (ZeroDivisionError,), 1),
    ],
)
def test_safe_access_no_exception(to_call, exceptions, expected):
    @safe_access(exceptions=exceptions)
    def to_call_wrapper():
        return to_call()

    assert to_call_wrapper() == expected


@pytest.mark.parametrize(
    "to_call, exceptions, default",
    [
        (lambda: {}["none_existing_key"], (KeyError,), None),
        (lambda: [][100], (IndexError,), 100),
        (lambda: 1 / 0, (ZeroDivisionError,), 0),
    ],
)
def test_safe_access_catch_exception(to_call, exceptions, default):
    @safe_access(exceptions=exceptions, default=default)
    def to_call_wrapper():
        return to_call()

    assert to_call_wrapper() == default


@pytest.mark.parametrize(
    "to_call, exceptions, expected_exception",
    [
        (lambda: {}["none_existing_key"], (ValueError,), KeyError),
        (lambda: [][100], (ValueError,), IndexError),
        (lambda: 1 / 0, (KeyError, IndexError), ZeroDivisionError),
    ],
)
def test_safe_access_not_catch_other_exceptions(to_call, exceptions, expected_exception):
    @safe_access(exceptions=exceptions)
    def to_call_wrapper():
        return to_call()

    with pytest.raises(expected_exception):
        to_call_wrapper()

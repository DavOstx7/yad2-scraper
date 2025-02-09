import io
from bs4 import BeautifulSoup

from yad2_scraper.category import Yad2Category, NextData


def test_from_html_io_with_stringio():
    html_content = "<html><body><div id='test'>Test</div></body></html>"
    html_io = io.StringIO(html_content)
    category = Yad2Category.from_html_io(html_io)
    assert isinstance(category, Yad2Category)
    assert category.soup.find("div", id="test") is not None


def test_from_html_io_with_bytesio():
    html_content = b"<html><body><div id='test'>Test</div></body></html>"
    html_io = io.BytesIO(html_content)
    category = Yad2Category.from_html_io(html_io)
    assert isinstance(category, Yad2Category)
    assert category.soup.find("div", id="test") is not None


def test_load_next_data_with_valid_json():
    html_content = """
    <html><head><script id="__NEXT_DATA__">{"key": "value"}</script></head><body></body></html>
    """
    soup = BeautifulSoup(html_content, "html.parser")
    category = Yad2Category(soup)
    next_data = category.load_next_data()
    assert isinstance(next_data, NextData)
    assert next_data.json == {"key": "value"}


def test_load_next_data_with_missing_tag():
    html_content = "<html><body></body></html>"
    soup = BeautifulSoup(html_content, "html.parser")
    category = Yad2Category(soup)
    next_data = category.load_next_data()
    assert next_data is None


def test_find_all_tags_by_class_substring():
    html_content = """
    <html><body><div class="item-tag">Item 1</div><div class="item-tag">Item 2</div></body></html>
    """
    soup = BeautifulSoup(html_content, "html.parser")
    category = Yad2Category(soup)
    tags = category.find_all_tags_by_class_substring("div", "item-tag")
    assert len(tags) == 2
    assert tags[0].text == "Item 1"
    assert tags[1].text == "Item 2"


def test_find_all_tags_by_class_substring_with_no_match():
    html_content = "<html><body><div class='other-tag'>Item 1</div></body></html>"
    soup = BeautifulSoup(html_content, "html.parser")
    category = Yad2Category(soup)
    tags = category.find_all_tags_by_class_substring("div", "item-tag")
    assert len(tags) == 0


def test_load_next_data_with_malformed_json():
    html_content = """
    <html><head><script id="NEXT_DATA_SCRIPT_ID">{"key": "value"</script></head><body></body></html>
    """
    soup = BeautifulSoup(html_content, "html.parser")
    category = Yad2Category(soup)
    next_data = category.load_next_data()
    assert next_data is None
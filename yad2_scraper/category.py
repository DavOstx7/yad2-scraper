import json
from bs4 import BeautifulSoup, Tag
from typing import Optional, List, Union, TextIO, BinaryIO

from yad2_scraper.next_data import NextData
from yad2_scraper.utils import find_all_html_tags_by_class_substring
from yad2_scraper.constants import NEXT_DATA_SCRIPT_ID


class Yad2Category:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    @classmethod
    def from_html_io(cls, html_io: Union[TextIO, BinaryIO]):
        html = html_io.read()
        soup = BeautifulSoup(html, "html.parser")
        return cls(soup)

    def load_next_data(self) -> Optional[NextData]:
        tag = self.soup.find("script", id=NEXT_DATA_SCRIPT_ID)
        return NextData(json.loads(tag.string)) if tag else None

    def find_all_tags_by_class_substring(self, tag_name: str, substring: str) -> List[Tag]:
        return find_all_html_tags_by_class_substring(self.soup, tag_name, substring)

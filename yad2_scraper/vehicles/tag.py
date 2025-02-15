from functools import cached_property
from bs4 import Tag
from typing import Optional

from yad2_scraper.utils import join_url, find_html_tag_by_class_substring
from yad2_scraper.vehicles.urls import VEHICLES_URL

YEAR_AND_HAND_TAG_SEPARATOR = " • "


class VehicleTag:
    def __init__(self, tag: Tag):
        self.tag = tag

    @cached_property
    def relative_link(self) -> str:
        return self.find_tag_by_class_substring("a", "itemLink")["href"]

    @property
    def page_link(self) -> str:
        return join_url(VEHICLES_URL, self.relative_link)

    @cached_property
    def image_url(self) -> str:
        return self.find_tag_by_class_substring("img", "image")["src"]

    @cached_property
    def model(self) -> str:
        return self.find_tag_by_class_substring("span", "heading").text.strip()

    @cached_property
    def marketing_text(self) -> str:
        return self.find_tag_by_class_substring("span", "marketingText").text.strip()

    @cached_property
    def year_and_hand_string(self) -> str:
        return self.find_tag_by_class_substring("span", "yearAndHand").text.strip()

    @property
    def year(self) -> int:
        year, _ = self.year_and_hand_string.split(YEAR_AND_HAND_TAG_SEPARATOR)
        return int(year)

    @property
    def hand(self) -> int:
        _, hand_string = self.year_and_hand_string.split(YEAR_AND_HAND_TAG_SEPARATOR)
        _, hand = hand_string.split()
        return int(hand)

    @cached_property
    def price_string(self) -> str:
        return self.find_tag_by_class_substring("span", "price").text.strip()

    @property
    def price(self) -> Optional[int]:
        try:
            price, _ = self.price_string.split()
            return int(price.replace(",", ""))
        except ValueError:
            return None

    def find_tag_by_class_substring(self, tag_name: str, substring: str) -> Tag:
        return find_html_tag_by_class_substring(self.tag, tag_name, substring)

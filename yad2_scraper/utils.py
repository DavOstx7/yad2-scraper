from fake_useragent import FakeUserAgent
from bs4 import BeautifulSoup, Tag
from typing import Union, List

fua = FakeUserAgent()


def get_random_user_agent() -> str:
    return fua.random


def format_attempt_log(attempt: int, max_attempts: int) -> str:
    return f"(attempt {attempt}/{max_attempts})"


def join_url(url: str, path: str) -> str:
    return url.rstrip("/") + "/" + path.lstrip("/")


def get_parent_url(url: str) -> str:
    if url.count("/") <= 2:
        return url

    return url.rstrip("/").rsplit("/", 1)[0]


def find_html_tag_by_class_substring(e: Union[BeautifulSoup, Tag], tag_name: str, substring: str) -> Tag:
    return e.find(tag_name, class_=lambda class_name: class_name and substring in class_name)


def find_all_html_tags_by_class_substring(e: Union[BeautifulSoup, Tag], tag_name: str, substring: str) -> List[Tag]:
    return e.find_all(tag_name, class_=lambda class_name: class_name and substring in class_name)

import functools
from bs4 import BeautifulSoup, Tag
from typing import Union, List, Tuple, Any


def any_param_specified(*params: Any) -> bool:
    return any(param is not None for param in params)


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


def safe_access(exceptions: Tuple = (), default: Any = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions:
                return default

        return wrapper

    return decorator

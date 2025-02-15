import functools
from bs4 import BeautifulSoup, Tag
from typing import Union, List, Tuple, Any

def any_param_specified(*params: Any) -> bool:
    """Check if any parameter is not None."""
    return any(param is not None for param in params)

def join_url(url: str, path: str) -> str:
    """Join a base URL with a path, ensuring proper slashes."""
    return url.rstrip("/") + "/" + path.lstrip("/")

def get_parent_url(url: str) -> str:
    """Return the parent URL by removing the last segment."""
    if url.count("/") <= 2:
        return url
    return url.rstrip("/").rsplit("/", 1)[0]

def find_html_tag_by_class_substring(e: Union[BeautifulSoup, Tag], tag_name: str, substring: str) -> Tag:
    """Find the first HTML tag with a class containing the given substring."""
    return e.find(tag_name, class_=lambda class_name: class_name and substring in class_name)

def find_all_html_tags_by_class_substring(e: Union[BeautifulSoup, Tag], tag_name: str, substring: str) -> List[Tag]:
    """Find all HTML tags with a class containing the given substring."""
    return e.find_all(tag_name, class_=lambda class_name: class_name and substring in class_name)

def safe_access(exceptions: Tuple = (), default: Any = None):
    """Decorator to safely execute a function, returning a default value on exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions:
                return default
        return wrapper
    return decorator
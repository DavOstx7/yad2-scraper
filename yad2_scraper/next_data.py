from datetime import datetime
from enum import Enum
from typing import List, Union

from yad2_scraper.utils import safe_access

FieldTypes = Union[str, int]

_safe_access_optional_keys = safe_access(exceptions=(KeyError, TypeError), default=None)


class SafeAccessOptionalKeysMeta(type):
    def __new__(cls, name, bases, dictionary):
        for attr_name, attr_value in dictionary.items():
            if callable(attr_value):  # Wrap methods
                dictionary[attr_name] = _safe_access_optional_keys(attr_value)
            elif isinstance(attr_value, property):  # Wrap properties
                dictionary[attr_name] = property(
                    _safe_access_optional_keys(attr_value.fget) if attr_value.fget else None,
                    _safe_access_optional_keys(attr_value.fset) if attr_value.fset else None,
                    _safe_access_optional_keys(attr_value.fdel) if attr_value.fdel else None,
                    attr_value.__doc__,
                )
        return super().__new__(cls, name, bases, dictionary)


class Field(str, Enum):
    ID = "id"
    TEXT = "text"
    ENGLISH_TEXT = "textEng"


def convert_string_date_to_datetime(date_string: str) -> datetime:
    return datetime.fromisoformat(date_string)


class NextData:
    def __init__(self, data: dict):
        self.data = data

    @property
    def json(self) -> dict:
        return self.data

    @property
    def queries(self) -> List[dict]:
        return self.data["props"]["pageProps"]["dehydratedState"]["queries"]

    def __getitem__(self, item):
        return self.data[item]

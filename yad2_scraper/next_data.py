from datetime import datetime
from enum import Enum
from typing import List, Union

FieldTypes = Union[str, int]


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

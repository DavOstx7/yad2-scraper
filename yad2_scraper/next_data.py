from enum import Enum
from typing import List, Union


class Field(str, Enum):
    ID = "id"
    TEXT = "text"
    ENGLISH_TEXT = "textEng"


FieldTypes = Union[str, int]


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

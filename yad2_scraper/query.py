from pydantic import BaseModel
from enum import Enum
from typing import Optional, Tuple

PriceRange = Tuple[int, int]


class OrderBy(int, Enum):
    DATE = 1
    PRICE_LOWEST_TO_HIGHEST = 3
    PRICE_HIGHEST_TO_LOWEST = 4
    ...


def format_number_range(number_range: Optional[Tuple[int, int]]) -> Optional[str]:
    if number_range is None:
        return None

    try:
        min_value, max_value = min(*number_range), max(*number_range)
    except TypeError:
        raise ValueError("Number range is incomplete, both values must be set")

    return f"{min_value}-{max_value}"


class QueryFilters(BaseModel):
    page: Optional[int] = None
    order_by: Optional[OrderBy] = None
    price_range: Optional[PriceRange] = None
    ...

    def to_dict_raw(self) -> dict:
        return {
            "page": self.page,
            "Order": self.order_by,
            "price": format_number_range(self.price_range)
        }

    # TODO: add helper methods for managing the attribute values

    def __iter__(self):
        for key, value in self.to_dict_raw().items():
            if value is not None:
                yield key, value

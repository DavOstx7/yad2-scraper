from pydantic import BaseModel
from enum import Enum
from typing import Optional, Tuple

NumberRange = Tuple[int, int]


class OrderBy(int, Enum):
    DATE = 1
    PRICE_LOWEST_TO_HIGHEST = 3
    PRICE_HIGHEST_TO_LOWEST = 4
    ...


def format_number_range(number_range: Optional[Tuple[int, int]]) -> Optional[str]:
    """Format a number range as 'min_value-max_value'."""
    if number_range is None:
        return None

    try:
        min_value, max_value = min(*number_range), max(*number_range)
    except TypeError:
        raise ValueError("Number range is incomplete, both values must be set")

    return f"{min_value}-{max_value}"


class QueryFilters(BaseModel):
    """Pydantic model representing query filters for querying a resource."""
    page: Optional[int] = None
    order_by: Optional[OrderBy] = None
    price_range: Optional[NumberRange] = None

    def to_params(self) -> dict:
        """Convert filter fields to query parameters."""
        return {
            "page": self.page,
            "Order": self.order_by,
            "price": format_number_range(self.price_range)
        }

    def to_clean_params(self):
        """Return query parameters excluding None values."""
        return {key: value for key, value in self.to_params().items() if value is not None}

    def __iter__(self):
        """Allow iteration over the clean query parameters."""
        yield from self.to_clean_params().items()

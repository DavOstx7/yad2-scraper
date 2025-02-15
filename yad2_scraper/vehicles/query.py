from enum import Enum
from typing import Optional

from yad2_scraper.query import QueryFilters, OrderBy, NumberRange, format_number_range


class OrderVehiclesBy(int, Enum):
    DATE = OrderBy.DATE
    PRICE_LOWEST_TO_HIGHEST = OrderBy.PRICE_LOWEST_TO_HIGHEST
    PRICE_HIGHEST_TO_LOWEST = OrderBy.PRICE_HIGHEST_TO_LOWEST
    DISTANCE_LOWEST_TO_HIGHEST = 5
    YEAR_HIGHEST_TO_LOWEST = 6


class VehiclesQueryFilters(QueryFilters):
    year_range: Optional[NumberRange] = None
    ...

    def to_params(self) -> dict:
        return {
            **super().to_params(),
            "year": format_number_range(self.year_range)
        }

# TODO: add QueryParams class for each vehicle category (some share the same attributes, sometimes with different enums)

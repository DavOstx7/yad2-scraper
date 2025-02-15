from enum import Enum
from typing import Optional

from yad2_scraper.query import QueryFilters, OrderBy, NumberRange, format_number_range


class OrderVehiclesBy(int, Enum):
    """Enum representing different order options for sorting vehicles."""
    DATE = OrderBy.DATE
    PRICE_LOWEST_TO_HIGHEST = OrderBy.PRICE_LOWEST_TO_HIGHEST
    PRICE_HIGHEST_TO_LOWEST = OrderBy.PRICE_HIGHEST_TO_LOWEST
    DISTANCE_LOWEST_TO_HIGHEST = 5
    YEAR_HIGHEST_TO_LOWEST = 6


class VehiclesQueryFilters(QueryFilters):
    """Pydantic model representing query filters for querying a vehicle resource."""
    year_range: Optional[NumberRange] = None

    def to_params(self) -> dict:
        """Convert filter fields to query parameters, including 'year'."""
        return {
            **super().to_params(),
            "year": format_number_range(self.year_range)
        }

# TODO: add QueryParams class for each vehicle category (some share the same attributes, sometimes with different enums)

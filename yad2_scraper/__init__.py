from typing import Optional, Type

from .scraper import Yad2Scraper, Category
from .query import QueryFilters, OrderBy, NumberRange
from .category import Yad2Category
from .next_data import NextData
from .utils import any_param_specified
from .vehicles import (
    Yad2VehiclesCategory,
    VehiclesQueryFilters,
    OrderVehiclesBy,
    VehicleCategory,
    get_vehicle_category_url
)

_default_scraper = None


def get_default_scraper() -> Yad2Scraper:
    global _default_scraper

    if not _default_scraper:
        _default_scraper = Yad2Scraper()

    return _default_scraper


def fetch_category(
        url: str,
        category_type: Type[Category] = Yad2Category,
        page: Optional[int] = None,
        order_by: Optional[OrderBy] = None,
        price_range: [NumberRange] = None
) -> Category:
    if any_param_specified(page, order_by, price_range):
        params = QueryFilters(page=page, order_by=order_by, price_range=price_range)
    else:
        params = None

    default_scraper = get_default_scraper()
    return default_scraper.fetch_category(url, category_type, params=params)


def fetch_vehicle_category(
        vehicle_category: VehicleCategory,
        page: Optional[int] = None,
        order_by: Optional[OrderVehiclesBy] = None,
        price_range: [NumberRange] = None,
        year_range: [NumberRange] = None
) -> Yad2VehiclesCategory:
    if any_param_specified(page, order_by, price_range, year_range):
        params = VehiclesQueryFilters(page=page, order_by=order_by, price_range=price_range, year_range=year_range)
    else:
        params = None

    url = get_vehicle_category_url(vehicle_category)
    default_scraper = get_default_scraper()
    return default_scraper.fetch_category(url, Yad2VehiclesCategory, params=params)

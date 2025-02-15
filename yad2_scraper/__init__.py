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
    """
    Retrieves the default instance of the Yad2Scraper. If an instance does not already exist, it will be created.

    Returns:
        Yad2Scraper: The default instance of the Yad2Scraper.

    Notes:
        The default scraper is a singleton instance that is reused across multiple calls.
    """
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
    """
    Fetches a specific category from the given URL, while applying optional filters.

    Args:
        url (str): The URL of the category to fetch.
        category_type (Type[Category], optional): The type of category to return (default is `Yad2Category`).
        page (Optional[int], optional): The page number for pagination (default is None).
        order_by (Optional[OrderBy], optional): The sorting order for the results (default is None).
        price_range (Optional[List[NumberRange]], optional): The price range filter for the results (default is None).

    Returns:
        Category: An instance of the specified `category_type`, populated with the fetched data.

    Notes:
        This method uses the default scraper to retrieve the category.
    """
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
    """
    Fetches a specific vehicle category, while applying optional filters.

    Args:
        vehicle_category (VehicleCategory): The vehicle category to fetch.
        page (Optional[int], optional): The page number for pagination (default is None).
        order_by (Optional[OrderVehiclesBy], optional): The sorting order for the results (default is None).
        price_range (Optional[List[NumberRange]], optional): The price range filter for the results (default is None).
        year_range (Optional[List[NumberRange]], optional): The year range filter for the results (default is None).

    Returns:
        Yad2VehiclesCategory: An instance of `Yad2VehiclesCategory`, populated with the fetched vehicle category data.

    Notes:
        This method uses the default scraper to fetch the vehicle category.
    """
    if any_param_specified(page, order_by, price_range, year_range):
        params = VehiclesQueryFilters(page=page, order_by=order_by, price_range=price_range, year_range=year_range)
    else:
        params = None

    url = get_vehicle_category_url(vehicle_category)
    default_scraper = get_default_scraper()
    return default_scraper.fetch_category(url, Yad2VehiclesCategory, params=params)

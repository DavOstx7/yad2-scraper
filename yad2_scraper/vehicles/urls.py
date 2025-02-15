from typing import Literal, get_args

from yad2_scraper.utils import join_url
from yad2_scraper.constants import BASE_URL

VEHICLES_URL = join_url(BASE_URL, "vehicles")

VehicleCategory = Literal["cars", "motorcycles", "scooters", "trucks", "watercraft", "others"]

_VALID_VEHICLE_CATEGORIES = get_args(VehicleCategory)


def get_vehicle_category_url(vehicle_category: VehicleCategory) -> str:
    """Generate the URL for the specified vehicle category."""
    if vehicle_category not in _VALID_VEHICLE_CATEGORIES:
        raise ValueError(
            f"Invalid vehicle category: {repr(vehicle_category)}. Expected one of {_VALID_VEHICLE_CATEGORIES}"
        )

    return join_url(VEHICLES_URL, vehicle_category)

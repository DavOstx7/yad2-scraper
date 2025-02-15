from typing import Literal, get_args

from yad2_scraper.utils import join_url
from yad2_scraper.constants import BASE_URL

VEHICLES_URL = join_url(BASE_URL, "vehicles")

VehicleType = Literal["cars", "motorcycles", "scooters", "trucks", "watercraft", "others"]

_VALID_VEHICLE_TYPES = get_args(VehicleType)


def get_vehicle_url(vehicle_type: VehicleType) -> str:
    if vehicle_type not in _VALID_VEHICLE_TYPES:
        raise ValueError(f"Invalid vehicle type: {repr(vehicle_type)}. Expected one of {_VALID_VEHICLE_TYPES}")
    return join_url(VEHICLES_URL, vehicle_type)

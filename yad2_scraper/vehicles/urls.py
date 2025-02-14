from typing import Literal

from yad2_scraper.utils import join_url
from yad2_scraper.constants import BASE_URL

VEHICLES_URL = join_url(BASE_URL, "vehicles")

VehicleType = Literal["cars", "motorcycles", "scooters", "trucks", "watercraft", "others"]


def get_vehicle_url(vehicle_type: VehicleType) -> str:
    return join_url(VEHICLES_URL, vehicle_type)

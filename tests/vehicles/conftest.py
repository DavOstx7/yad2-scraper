import pytest

from pathlib import Path
from typing import List
from yad2_scraper.vehicles import Yad2VehiclesCategory, VehicleTag, VehiclesNextData


@pytest.fixture(scope="session")
def cars_category() -> Yad2VehiclesCategory:
    html_path = Path(__file__).parent.parent / "data" / "cars_category.html"
    with html_path.open("rb") as file:
        return Yad2VehiclesCategory.from_html_io(file)


@pytest.fixture(scope="session")
def cars_tags(cars_category) -> List[VehicleTag]:
    return cars_category.get_vehicle_tags()


@pytest.fixture(scope="session")
def cars_next_data(cars_category) -> VehiclesNextData:
    return cars_category.load_next_data()

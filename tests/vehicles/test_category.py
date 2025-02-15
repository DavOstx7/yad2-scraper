import io
from yad2_scraper.vehicles.category import Yad2VehiclesCategory

EXPECTED_VEHICLES_COUNT = 40


def test_get_vehicle_tags(cars_category):
    tags = cars_category.get_vehicle_tags()
    assert len(tags) == EXPECTED_VEHICLES_COUNT


def test_load_next_data(cars_category):
    next_data = cars_category.load_next_data()
    assert len(list(next_data.iterate_vehicles())) == EXPECTED_VEHICLES_COUNT


def test_load_next_data_no_data():
    empty_bytes_io = io.BytesIO()
    category = Yad2VehiclesCategory.from_html_io(empty_bytes_io)
    assert not category.load_next_data()

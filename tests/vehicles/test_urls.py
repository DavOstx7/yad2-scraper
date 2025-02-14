import pytest

from yad2_scraper.vehicles.urls import get_vehicle_url, VEHICLES_URL


@pytest.mark.parametrize(
    "vehicle_type, expected_url",
    [
        ("cars", f"{VEHICLES_URL}/cars"),
        ("motorcycles", f"{VEHICLES_URL}/motorcycles"),
        ("scooters", f"{VEHICLES_URL}/scooters"),
        ("trucks", f"{VEHICLES_URL}/trucks"),
        ("watercraft", f"{VEHICLES_URL}/watercraft"),
        ("others", f"{VEHICLES_URL}/others"),
    ],
)
def test_get_vehicle_url(vehicle_type, expected_url):
    assert get_vehicle_url(vehicle_type) == expected_url


def test_get_vehicle_url_invalid():
    with pytest.raises(ValueError):
        get_vehicle_url("invalid_vehicle_type")

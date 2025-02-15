from yad2_scraper.query import OrderBy
from yad2_scraper.vehicles.query import VehiclesQueryFilters, OrderVehiclesBy


def test_vehicles_query_filters_to_params():
    filters = VehiclesQueryFilters(page=1, order_by=OrderVehiclesBy.DATE, year_range=(2010, 2020))
    result = filters.to_params()

    assert result["page"] == 1
    assert result["Order"] == OrderVehiclesBy.DATE
    assert result["year"] == "2010-2020"


def test_vehicles_query_filters_to_params_with_none_values():
    filters = VehiclesQueryFilters(page=None, order_by=None, year_range=None)
    result = filters.to_params()

    assert "page" in result
    assert "Order" in result
    assert "year" in result


def test_vehicles_query_filters_to_clean_params():
    filters = VehiclesQueryFilters(page=None, order_by=None, year_range=None)
    result = filters.to_clean_params()
    assert result == {}


def test_vehicles_query_filters_iter():
    filters = VehiclesQueryFilters(page=None, order_by=OrderVehiclesBy.DATE, year_range=(2015, 2021))
    result = dict(filters)

    assert result == {
        "Order": OrderVehiclesBy.DATE,
        "year": "2015-2021"
    }


def test_vehicles_query_filters_immutability():
    filters = VehiclesQueryFilters(page=1, order_by=OrderVehiclesBy.DATE, year_range=(2005, 2015))
    result = filters.to_params()
    result["page"] = 2
    assert filters.page == 1


def test_order_vehicles_by_enum():
    # Ensure values inherited from OrderBy
    assert OrderVehiclesBy.DATE == OrderBy.DATE
    assert OrderVehiclesBy.PRICE_LOWEST_TO_HIGHEST == OrderBy.PRICE_LOWEST_TO_HIGHEST
    assert OrderVehiclesBy.PRICE_HIGHEST_TO_LOWEST == OrderBy.PRICE_HIGHEST_TO_LOWEST

    # Ensure custom values
    assert OrderVehiclesBy.DISTANCE_LOWEST_TO_HIGHEST.value == 5
    assert OrderVehiclesBy.YEAR_HIGHEST_TO_LOWEST.value == 6

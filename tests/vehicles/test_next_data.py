import pytest
from typing import List, Tuple, Callable, Any

from yad2_scraper.next_data import Field

Method = Callable[[Field], Any]


@pytest.fixture
def vehicle_data_public_methods(cars_next_data) -> List[Tuple[str, Method]]:
    methods = []

    for obj in cars_next_data.iterate_vehicles():
        for attribute_name in dir(obj):
            if attribute_name.startswith("_"):
                continue

            attribute = getattr(obj, attribute_name)
            if callable(attribute):
                method_name, bound_method = attribute_name, attribute
                methods.append((method_name, bound_method))

    return methods


@pytest.fixture
def vehicle_data_public_properties(cars_next_data) -> List[Tuple[str, Any]]:
    properties = []

    for obj in cars_next_data.iterate_vehicles():
        for attribute_name in dir(obj):
            if attribute_name.startswith("_"):
                continue

            attribute = getattr(obj, attribute_name)
            if not callable(attribute):
                property_name, property_value = attribute_name, attribute
                properties.append((property_name, property_value))

    return properties


def test_vehicle_data_methods(vehicle_data_public_methods):
    returned_none_methods = set()
    returned_value_methods = set()

    for method_name, bound_method in vehicle_data_public_methods:
        ret = bound_method(Field.ID)
        if ret is None:
            returned_none_methods.add(method_name)
        else:
            returned_value_methods.add(method_name)

    methods_that_only_return_none = returned_none_methods - returned_value_methods
    assert not methods_that_only_return_none


def test_vehicle_data_properties(vehicle_data_public_properties):
    returned_none_properties = set()
    returned_value_properties = set()

    for property_name, property_value in vehicle_data_public_properties:
        if property_value is None:
            returned_none_properties.add(property_name)
        else:
            returned_value_properties.add(property_name)

    properties_that_only_return_none = returned_none_properties - returned_value_properties
    assert not properties_that_only_return_none

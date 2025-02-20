import itertools
from datetime import datetime
from typing import List, Any, Iterator, Optional

from yad2_scraper.next_data import (
    SafeAccessOptionalKeysMeta,
    NextData,
    Field,
    FieldTypes,
    convert_string_date_to_datetime
)
from yad2_scraper.utils import join_url
from yad2_scraper.vehicles.urls import VEHICLES_URL


class VehicleData(metaclass=SafeAccessOptionalKeysMeta):
    """Represents the data for a single vehicle."""

    def __init__(self, data: dict):
        self.data = data

    @property
    def token(self) -> str:
        return self["token"]

    @property
    def page_link(self) -> str:
        return join_url(VEHICLES_URL, f"item/{self.token}")

    @property
    def price(self) -> int:
        return self["price"]

    @property
    def customer(self) -> dict:
        return self["customer"]

    @property
    def customer_name(self) -> str:
        return self.customer["name"]

    @property
    def customer_phone(self) -> str:
        return self.customer["phone"]

    @property
    def address(self) -> dict:
        return self["address"]

    def top_area(self, field: Field = Field.TEXT) -> Optional[FieldTypes]:
        return self["address"]["topArea"][field]

    def area(self, field: Field = Field.TEXT) -> Optional[FieldTypes]:
        return self["address"]["area"][field]

    def city(self, field: Field = Field.TEXT) -> Optional[FieldTypes]:
        return self["address"]["city"][field]

    @property
    def metadata(self) -> dict:
        return self["metaData"]

    @property
    def video(self) -> str:
        return self.metadata["video"]

    @property
    def cover_image(self) -> str:
        return self.metadata["coverImage"]

    @property
    def images(self) -> str:
        return self.metadata["images"]

    @property
    def description(self) -> str:
        return self.metadata["description"]

    @property
    def dates(self) -> dict:
        return self["dates"]

    @property
    def updated_at(self) -> datetime:
        return convert_string_date_to_datetime(self.dates["updatedAt"])

    @property
    def created_at(self) -> datetime:
        return convert_string_date_to_datetime(self.dates["createdAt"])

    @property
    def ends_at(self) -> datetime:
        return convert_string_date_to_datetime(self.dates["endsAt"])

    @property
    def rebounced_at(self) -> datetime:
        return convert_string_date_to_datetime(self.dates["rebouncedAt"])

    def manufacturer(self, field: Field = Field.TEXT) -> Optional[FieldTypes]:
        return self["manufacturer"][field]

    def color(self, field: Field = Field.TEXT) -> Optional[FieldTypes]:
        return self["color"][field]

    @property
    def km(self) -> Optional[int]:
        return self["km"]

    @property
    def hand(self, field: Field = Field.ID) -> Optional[FieldTypes]:
        return self["hand"][field]

    @property
    def engine_volume(self) -> Optional[int]:
        return self["engineVolume"]

    @property
    def horse_power(self) -> Optional[int]:
        return self["horsePower"]

    @property
    def previous_owner(self, field: Field = Field.TEXT) -> Optional[FieldTypes]:
        return self["previousOwner"][field]

    @property
    def above_price(self) -> Optional[int]:
        return self["abovePrice"]

    @property
    def tags(self) -> List[dict]:
        return self["tags"]

    @property
    def is_contact_lead_supported(self) -> Optional[bool]:
        return self["isContactLeadSupported"]

    @property
    def vehicle_dates(self) -> dict:
        return self["vehicleDates"]

    @property
    def year_of_production(self) -> Optional[int]:
        return self.vehicle_dates["yearOfProduction"]

    @property
    def month_of_production(self) -> Optional[int]:
        return self.vehicle_dates["monthOfProduction"]["id"]

    @property
    def test_date(self) -> Optional[datetime]:
        return convert_string_date_to_datetime(self.vehicle_dates["testDate"])

    def model(self, field: Field = Field.TEXT) -> Optional[FieldTypes]:
        return self["model"][field]

    @property
    def sub_model(self) -> Optional[str]:
        return self["subModel"]

    def gear_box(self, field: Field = Field.TEXT) -> Optional[FieldTypes]:
        return self["gearBox"][field]

    def car_family_types(self, field: Field = Field.TEXT) -> Optional[List[FieldTypes]]:
        return [obj[field] for obj in self["carFamilyType"]]

    def engine_type(self, field: Field = Field.TEXT) -> Optional[FieldTypes]:
        return self["engineType"][field]

    @property
    def seats(self) -> Optional[int]:
        return self["seats"]

    @property
    def number_of_doors(self) -> Optional[int]:
        return self["numberOfDoors"]

    @property
    def owner(self) -> Optional[str]:
        return self["owner"]["text"]

    @property
    def body_type(self) -> Optional[str]:
        return self["bodyType"]["text"]

    @property
    def combined_fuel_consumption(self) -> Optional[float]:
        return self["combinedFuelConsumption"]

    @property
    def power_train_architecture(self) -> Optional[str]:
        return self["powertrainArchitecture"]

    def car_tags(self, field: Field = Field.TEXT) -> Optional[List[FieldTypes]]:
        return [obj[field] for obj in self["carTag"]]

    @property
    def specification(self) -> dict:
        return self["specification"]

    @property
    def has_air_conditioner(self) -> Optional[bool]:
        return self.specification["airConditioner"]

    @property
    def has_power_steering(self) -> Optional[bool]:
        return self.specification["powerSteering"]

    @property
    def has_magnesium_wheel(self) -> Optional[bool]:
        return self.specification["magnesiumWheel"]

    @property
    def has_tire_pressure_monitoring_system(self) -> Optional[bool]:
        return self.specification["tirePressureMonitoringSystem"]

    @property
    def has_abs(self) -> Optional[bool]:
        return self.specification["abs"]

    @property
    def air_bags(self) -> Optional[int]:
        return self.specification["airBags"]

    @property
    def has_control_stability(self) -> Optional[bool]:
        return self.specification["controlStability"]

    @property
    def has_electric_window(self) -> Optional[int]:
        return self.specification["electricWindow"]

    @property
    def has_breaking_assist_system(self) -> Optional[bool]:
        return self.specification["breakingAssistSystem"]

    @property
    def has_reverse_camera(self) -> Optional[bool]:
        return self.specification["reverseCamera"]

    @property
    def has_adaptive_cruise_control(self) -> Optional[bool]:
        return self.specification["adaptiveCruiseControl"]

    @property
    def has_high_beams_auto_control(self) -> Optional[bool]:
        return self.specification["highBeamsAutoControl"]

    @property
    def has_blind_spot_assist(self) -> Optional[bool]:
        return self.specification["blindSpotAssist"]

    @property
    def has_identify_pedestrians(self) -> Optional[bool]:
        return self.specification["identifyPedestrians"]

    @property
    def has_seat_belts_sensors(self) -> Optional[bool]:
        return self.specification["seatBeltsSensors"]

    @property
    def has_identifying_dangerous_nearing(self) -> Optional[bool]:
        return self.specification["identifyingDangerousNearing"]

    @property
    def has_auto_lighting_in_forward(self) -> Optional[bool]:
        return self.specification["autoLightingInForward"]

    @property
    def has_identify_traffic_signs(self) -> Optional[bool]:
        return self.specification["identifyTrafficSigns"]

    def ignition(self, field: Field = Field.TEXT) -> Optional[FieldTypes]:
        return self.specification["ignition"][field]

    @property
    def safety_points(self) -> Optional[int]:
        return self.specification["safetyPoints"]

    @property
    def is_handicapped_friendly(self) -> Optional[bool]:
        return self.specification["isHandicappedFriendly"]

    @property
    def has_sun_roof(self) -> Optional[bool]:
        return self.specification["sunRoof"]

    @property
    def is_turbo(self) -> Optional[bool]:
        return self.specification["isTurbo"]

    @property
    def has_road_deviation_control(self) -> Optional[bool]:
        return self.specification["roadDeviationControl"]

    @property
    def has_forward_distance_monitor(self) -> Optional[bool]:
        return self.specification["forwardDistanceMonitor"]

    @property
    def has_box(self) -> Optional[bool]:
        return self.specification["box"]

    def __getitem__(self, key: str) -> Any:
        return self.data[key]


class VehiclesNextData(NextData):
    """Represents structured Next.js data of a specific vehicle category."""

    def get_data(self) -> List[VehicleData]:
        """Extract and return a list of vehicle-data objects from the stored queries."""
        data_list = []

        for query in self.queries:
            data = query["state"].get("data")

            if not data or isinstance(data, list):
                continue

            for vehicle_data in itertools.chain.from_iterable(data.values()):
                if isinstance(vehicle_data, dict):
                    data_list.append(VehicleData(vehicle_data))

        return data_list

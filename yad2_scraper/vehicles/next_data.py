import itertools
from datetime import datetime
from typing import List, Any, Iterator

from yad2_scraper.next_data import NextData, Field, FieldTypes, convert_string_date_to_datetime
from yad2_scraper.utils import join_url
from yad2_scraper.vehicles.urls import VEHICLES_URL


class VehicleData:
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

    def top_area(self, field: Field = Field.TEXT) -> FieldTypes:
        return self["address"]["topArea"][field]

    def area(self, field: Field = Field.TEXT) -> FieldTypes:
        return self["address"]["area"][field]

    def city(self, field: Field = Field.TEXT) -> FieldTypes:
        return self["address"]["city"][field]

    @property
    def metadata(self) -> dict:
        return self["metadata"]

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

    def manufacturer(self, field: Field = Field.TEXT) -> FieldTypes:
        return self["manufacturer"][field]

    def color(self, field: Field = Field.TEXT) -> FieldTypes:
        return self["color"][field]

    @property
    def km(self) -> int:
        return self["km"]

    @property
    def hand(self, field: Field = Field.ID) -> FieldTypes:
        return self["hand"][field]

    @property
    def engine_volume(self) -> int:
        return self["engineVolume"]

    @property
    def horse_power(self) -> int:
        return self["horsePower"]

    @property
    def previous_owner(self, field: Field = Field.TEXT) -> FieldTypes:
        return self["previousOwner"][field]

    @property
    def above_price(self) -> int:
        return self["abovePrice"]

    @property
    def tags(self) -> List[dict]:
        return self["tags"]

    @property
    def is_contact_lead_supported(self) -> bool:
        return self["isContactLeadSupported"]

    @property
    def vehicle_dates(self) -> dict:
        return self["vehicleDates"]

    @property
    def year_of_production(self) -> int:
        return self.vehicle_dates["yearOfProduction"]

    @property
    def month_of_production(self) -> int:
        return self.vehicle_dates["monthOfProduction"]["id"]

    @property
    def test_date(self) -> datetime:
        return convert_string_date_to_datetime(self.vehicle_dates["testDate"])

    def model(self, field: Field = Field.TEXT) -> FieldTypes:
        return self["model"][field]

    @property
    def sub_model(self) -> str:
        return self["subModel"]

    def gear_box(self, field: Field = Field.TEXT) -> FieldTypes:
        return self["gearBox"][field]

    def car_family_types(self, field: Field = Field.TEXT) -> List[FieldTypes]:
        return [obj[field] for obj in self["carFamilyType"]]

    def engine_type(self, field: Field = Field.TEXT) -> FieldTypes:
        return self["engineType"][field]

    @property
    def seats(self) -> int:
        return self["seats"]

    @property
    def number_of_doors(self) -> int:
        return self["numberOfDoors"]

    @property
    def owner(self) -> str:
        return self["owner"]["text"]

    @property
    def body_type(self) -> str:
        return self["bodyType"]["text"]

    @property
    def combined_fuel_consumption(self) -> float:
        return self["combinedFuelConsumption"]

    @property
    def power_train_architecture(self) -> str:
        return self["powertrainArchitecture"]

    def car_tags(self, field: Field = Field.TEXT) -> List[FieldTypes]:
        return [obj[field] for obj in self["carTag"]]

    @property
    def specifications(self) -> dict:
        return self["specifications"]

    @property
    def has_air_conditioner(self) -> bool:
        return self.specifications["airConditioner"]

    @property
    def has_power_steering(self) -> bool:
        return self.specifications["powerSteering"]

    @property
    def has_magnesium_wheel(self) -> bool:
        return self.specifications["magnesiumWheel"]

    @property
    def has_tire_pressure_monitoring_system(self) -> bool:
        return self.specifications["tirePressureMonitoringSystem"]

    @property
    def has_abs(self) -> bool:
        return self.specifications["abs"]

    @property
    def air_bags(self) -> int:
        return self.specifications["airBags"]

    @property
    def has_control_stability(self) -> bool:
        return self.specifications["controlStability"]

    @property
    def has_electric_window(self) -> int:
        return self.specifications["electricWindow"]

    @property
    def has_breaking_assist_system(self) -> bool:
        return self.specifications["breakingAssistSystem"]

    @property
    def has_reverse_camera(self) -> bool:
        return self.specifications["reverseCamera"]

    @property
    def has_adaptive_cruise_control(self) -> bool:
        return self.specifications["adaptiveCruiseControl"]

    @property
    def has_high_beams_auto_control(self) -> bool:
        return self.specifications["highBeamsAutoControl"]

    @property
    def has_blind_spot_assist(self) -> bool:
        return self.specifications["blindSpotAssist"]

    @property
    def has_identify_pedestrians(self) -> bool:
        return self.specifications["identifyPedestrians"]

    @property
    def has_seat_belts_sensors(self) -> bool:
        return self.specifications["seatBeltsSensors"]

    @property
    def has_identifying_dangerous_nearing(self) -> bool:
        return self.specifications["identifyingDangerousNearing"]

    @property
    def has_auto_lighting_in_forward(self) -> bool:
        return self.specifications["autoLightingInForward"]

    @property
    def has_identify_traffic_signs(self) -> bool:
        return self.specifications["identifyTrafficSigns"]

    def ignition(self, field: Field.TEXT) -> FieldTypes:
        return self.specifications[field]

    @property
    def safety_points(self) -> int:
        return self.specifications["safetyPoints"]

    @property
    def is_handicapped_friendly(self) -> bool:
        return self.specifications["isHandicappedFriendly"]

    @property
    def has_sun_roof(self) -> bool:
        return self.specifications["sunRoof"]

    @property
    def is_turbo(self) -> bool:
        return self.specifications["isTurbo"]

    @property
    def has_road_deviation_control(self) -> bool:
        return self.specifications["roadDeviationControl"]

    @property
    def has_forward_distance_monitor(self) -> bool:
        return self.specifications["forwardDistanceMonitor"]

    @property
    def has_box(self) -> bool:
        return self.specifications["box"]

    def __getitem__(self, key: str) -> Any:
        return self.data[key]


class VehiclesNextData(NextData):
    def iterate_vehicles(self) -> Iterator[VehicleData]:
        for query in self.queries:
            data = query["state"].get("data")

            if not data or isinstance(data, list):
                continue

            for vehicle_data in itertools.chain.from_iterable(data.values()):
                if isinstance(vehicle_data, dict):
                    yield VehicleData(vehicle_data)

    def __getitem__(self, item):
        return self.data[item]

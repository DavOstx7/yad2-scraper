from typing import List, Optional

from yad2_scraper.category import Yad2Category
from yad2_scraper.vehicles.tag import VehicleTag
from yad2_scraper.vehicles.next_data import VehiclesNextData


class Yad2VehiclesCategory(Yad2Category):
    def get_vehicle_tags(self) -> List[VehicleTag]:
        """Retrieve a and return list of vehicle tags from the current category."""
        tags = self.find_all_tags_by_class_substring("div", "feedItemBox")
        return [VehicleTag(tag) for tag in tags]

    def load_next_data(self) -> Optional[VehiclesNextData]:
        """Extract and parse Next.js data from the current vehicle page."""
        next_data = super().load_next_data()
        return VehiclesNextData(next_data) if next_data else None

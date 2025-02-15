# Yad2 Scraper

A Python package for scraping listings from [Yad2](https://www.yad2.co.il/), Israel's leading classifieds
platform. This package provides a simple and flexible interface to fetch data,
filter results, and extract relevant information.

---

## Features

- **Fetch Listings**: Retrieve listings by category (e.g., vehicles, real-estate, etc.).
- **Filter Results**: Apply filters such as price range, year range, and sorting order.
- **Dynamic URL Generation**: Generate URLs for specific categories and filters.
- **Type-Safe API**: Uses Python type hints (`Literal`, `Optional`, etc.) for better code clarity and safety.
- **Extensible**: Easily extendable to support additional categories and filters.

---

## Installation

Install the package using `pip`:

```bash
pip install yad2-scraper
```

## Usage

### Fetching Category Listings

To fetch any yad2 category, use the `fetch_category` function:

```python
from yad2_scraper import fetch_category, Yad2Category

# Fetch real estate listings
real_estate_category_page1 = fetch_category("https://www.yad2.co.il/realestate/forsale", Yad2Category, page=1)
...
real_estate_category_page2 = fetch_category("https://www.yad2.co.il/realestate/forsale", Yad2Category, page=2)
...
```

__NOTE__: Unfortunately, the current package mainly has support for the vehicle category.

### Fetching Vehicle Listings

To fetch vehicle listings for a specific category, use the `fetch_vehicle_category` function:

```python
from yad2_scraper import fetch_vehicle_category, OrderVehiclesBy

# Fetch car listings
cars_category = fetch_vehicle_category("cars")

for car_data in cars_category.load_next_data().iterate_vehicles():
    print(car_data.model())
    print(car_data.test_date)
    print(car_data.price)
    ...

# Fetch motorcycle listings with filters
motorcycle_categories = fetch_vehicle_category(
    "motorcycles",
    price_range=(5000, 15000),
    year_range=(2010, 2020),
    order_by=OrderVehiclesBy.PRICE_LOWEST_TO_HIGHEST
)

for motorcycle_tag in motorcycle_categories.get_vehicle_tags():
    print(motorcycle_tag.page_link)
    print(motorcycle_tag.hand)
    print(motorcycle_tag.price)
    ...
```

#### Generating Vehicle URLs

To generate a URL for a specific vehicle category, use the `get_vehicle_category_url` function:

```python
from yad2_scraper import get_vehicle_category_url, VehicleCategory

# Get URL for car listings
car_url = get_vehicle_category_url(VehicleCategory.CARS)
print(car_url)  # Output: https://www.yad2.co.il/vehicles/cars
```

#### Using Filters

Apply filters to refine your search results:

```python
from yad2_scraper import fetch_vehicle_category

# Fetch truck listings with price and year filters
truck_listings = fetch_vehicle_category(
    "trucks",
    price_range=(20000, 50000),
    year_range=(2015, 2022)
)
```

### The Scraper Object

The `Yad2Scraper` class is the core of the package.
It handles HTTP requests, parses responses, and provides methods to fetch and filter vehicle listings.

#### Creating a Scraper Instance

You can create a `Yad2Scraper` instance manually or use the default scraper provided by the package:

```python
from yad2_scraper import Yad2Scraper, get_default_scraper

# Create a custom scraper instance
scraper = Yad2Scraper(request_defaults={"timeout": 10}, randomize_user_agent=True, ...)

# Use the default scraper
default_scraper = get_default_scraper()
```

#### Fetching Listings

The `fetch_category` method is used to fetch listings for a specific category.
It takes a URL, a `Category` type, and optionally query params as arguments:

```python
from yad2_scraper import Yad2Scraper, Yad2VehiclesCategory, VehiclesQueryFilters

# Fetch cars category
scraper = Yad2Scraper()
cars_category = scraper.fetch_category("https://www.yad2.co.il/vehicles/cars", Yad2VehiclesCategory, )
```

#### Applying Filters

You can pass `QueryFilters` or `VehiclesQueryFilters` to the `fetch_category` method to apply filters:

```python
from yad2_scraper import Yad2Scraper, Yad2VehiclesCategory, VehiclesQueryFilters, OrderVehiclesBy

# Fetch motorcycles category with filters
scraper = Yad2Scraper()
query_filters = VehiclesQueryFilters(
    price_range=(5000, 15000),
    year_range=(2010, 2020),
    order_by=OrderVehiclesBy.PRICE_HIGHEST_TO_LOWEST
)
motorcycle_listings = scraper.fetch_category(
    "https://www.yad2.co.il/vehicles/motorcycles",
    Yad2VehiclesCategory,
    params=query_filters
)
```

#### Using the Default Scraper

The package provides a default scraper instance that you can use without creating a new `Yad2Scraper` object:

```python
from yad2_scraper import get_default_scraper

# Use the default scraper
default_scraper = get_default_scraper()
```

## Contributing

Contributions are welcomed! Here’s how you can get started:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Write tests for your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For questions, issues, or feature requests, please open an issue on the GitHub repository.
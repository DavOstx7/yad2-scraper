# Yad2 Scraper

A Python package for scraping listings from [Yad2](https://www.yad2.co.il/), Israel's leading classifieds platform.
This package provides a simple and flexible interface to fetch data, filter results, and extract relevant information.

__NOTE__: Currently, the package primarily supports the **vehicles category**.
Support for additional categories may be added in future updates.

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

To fetch any category, use the `fetch_category` function:

```python
from yad2_scraper import fetch_category, Yad2Category

# Fetch real estate category (returns a generic Yad2Category object)
real_estate_page1 = fetch_category("https://www.yad2.co.il/realestate/forsale", page=1)
...
real_estate_page2 = fetch_category("https://www.yad2.co.il/realestate/forsale", page=2)
...
```

### Fetching Vehicle Listings

To fetch vehicle listings for a specific category, use the `fetch_vehicle_category` function:

```python
from yad2_scraper import fetch_vehicle_category, OrderVehiclesBy, Field

# Fetch cars category
cars_category = fetch_vehicle_category("cars")

for car_data in cars_category.load_next_data().get_data():
    print(car_data.model(Field.ENGLISH_TEXT))
    print(car_data.test_date)
    print(car_data.price)
    ...

# Fetch motorcycles category
motorcycle_category = fetch_vehicle_category(
    "motorcycles",
    price_range=(5000, 15000),
    year_range=(2010, 2020),
    order_by=OrderVehiclesBy.PRICE_LOWEST_TO_HIGHEST
)

for motorcycle_tag in motorcycle_category.get_tags():
    print(motorcycle_tag.page_link)
    print(motorcycle_tag.hand)
    print(motorcycle_tag.price)
    ...
```

### The Scraper Object

The `Yad2Scraper` class is the core of the package.
It handles HTTP requests, parses responses, and provides methods to fetch and filter vehicle listings.

#### Creating a Scraper Instance

You can create a `Yad2Scraper` instance manually or use the default scraper provided by the package:

```python
from yad2_scraper import Yad2Scraper, get_default_scraper

# Create a custom scraper instance
scraper = Yad2Scraper()

# Use the default scraper
default_scraper = get_default_scraper()
```

#### Fetching Category Listings

The `fetch_category` method is used to fetch listings for a specific category.
It takes a URL, a `Category` type, and optionally query params as arguments:

```python
from yad2_scraper import Yad2Scraper, Yad2Category, QueryFilters, OrderBy
from yad2_scraper.vehicles import (
    Yad2VehiclesCategory,
    VehiclesQueryFilters,
    OrderVehiclesBy,
    get_vehicle_category_url
)

scraper = Yad2Scraper(request_defaults={"timeout": 5}, max_request_attempts=3)

# Fetch businesses-for-sale category with filters
url = "https://www.yad2.co.il/products/businesses-for-sale"
query_filters = QueryFilters(price_range=(10000, 250000), order_by=OrderBy.PRICE_LOWEST_TO_HIGHEST)
businesses_for_sale_category = scraper.fetch_category(url, Yad2Category, params=query_filters)

# Fetch watercraft category with filters
url = get_vehicle_category_url("watercraft")
query_filters = VehiclesQueryFilters(year_range=(2010, 2020), order_by=OrderVehiclesBy.DATE)
watercraft_category = scraper.fetch_category(url, Yad2VehiclesCategory, params=query_filters)
```

#### Features & Functionality

The `Yad2Scraper` class provides various attributes and methods to customize and extend its functionality.
For detailed usage and examples, refer to the code documentation.

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
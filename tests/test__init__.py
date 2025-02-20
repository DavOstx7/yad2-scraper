import pytest
from unittest.mock import patch, MagicMock
from yad2_scraper import (
    get_default_scraper,
    fetch_category,
    fetch_vehicle_category,
    Yad2Scraper,
    Yad2Category, QueryFilters, OrderBy,
    Yad2VehiclesCategory, VehiclesQueryFilters, OrderVehiclesBy
)


@pytest.fixture
def mock_scraper():
    return MagicMock(spec=Yad2Scraper)


@pytest.fixture
def mock_category():
    return MagicMock(spec=Yad2Category)


@pytest.fixture
def mock_any_param_specified():
    with patch("yad2_scraper.any_param_specified") as mock:
        yield mock


@pytest.fixture
def mock_get_vehicle_category_url():
    with patch("yad2_scraper.get_vehicle_category_url") as mock:
        yield mock


# Tests for get_default_scraper
def test_get_default_scraper_initializes_scraper(mock_scraper):
    with patch("yad2_scraper.Yad2Scraper", return_value=mock_scraper):
        scraper = get_default_scraper()
        assert scraper == mock_scraper


def test_get_default_scraper_returns_existing_scraper(mock_scraper):
    with patch("yad2_scraper._default_scraper", mock_scraper):
        scraper = get_default_scraper()
        assert scraper == mock_scraper


# Tests for fetch_category
def test_fetch_category_with_params(mock_scraper, mock_category, mock_any_param_specified):
    mock_any_param_specified.return_value = True
    url = "http://example.com"
    page = 1
    order_by = OrderBy.DATE
    price_range = 1000, 5000

    with patch("yad2_scraper.get_default_scraper", return_value=mock_scraper):
        fetch_category(
            url,
            mock_category,
            page=page, order_by=order_by, price_range=price_range
        )

        mock_scraper.fetch_category.assert_called_once_with(
            url,
            mock_category,
            params=QueryFilters(page=page, order_by=order_by, price_range=price_range),
        )


def test_fetch_category_without_params(mock_scraper, mock_category, mock_any_param_specified):
    mock_any_param_specified.return_value = False
    url = "http://example.com"

    with patch("yad2_scraper.get_default_scraper", return_value=mock_scraper):
        fetch_category(url, mock_category)

        mock_scraper.fetch_category.assert_called_once_with(
            url,
            mock_category,
            params=None
        )


# Tests for fetch_vehicle_category
def test_fetch_vehicle_category_with_params(
        mock_scraper,
        mock_any_param_specified,
        mock_get_vehicle_category_url
):
    mock_any_param_specified.return_value = True
    mock_get_vehicle_category_url.return_value = "http://example.com/vehicles"
    vehicle_category = "cars"
    page = 1
    order_by = OrderVehiclesBy.PRICE_LOWEST_TO_HIGHEST
    price_range = 1000, 5000
    year_range = 2000, 2020

    with patch("yad2_scraper.get_default_scraper", return_value=mock_scraper):
        fetch_vehicle_category(
            vehicle_category,
            page=page, order_by=order_by, price_range=price_range, year_range=year_range
        )

        mock_scraper.fetch_category.assert_called_once_with(
            "http://example.com/vehicles",
            Yad2VehiclesCategory,
            params=VehiclesQueryFilters(page=page, order_by=order_by, price_range=price_range, year_range=year_range)
        )


def test_fetch_vehicle_category_without_params(
        mock_scraper,
        mock_any_param_specified,
        mock_get_vehicle_category_url
):
    mock_any_param_specified.return_value = False
    mock_get_vehicle_category_url.return_value = "http://example.com/vehicles"
    vehicle_category = "cars"

    with patch("yad2_scraper.get_default_scraper", return_value=mock_scraper):
        fetch_vehicle_category(vehicle_category)

        mock_scraper.fetch_category.assert_called_once_with(
            "http://example.com/vehicles",
            Yad2VehiclesCategory,
            params=None
        )

import pytest

from yad2_scraper.query import QueryFilters, OrderBy, format_number_range


def test_query_filters_to_params():
    filters = QueryFilters(page=1, order_by=OrderBy.DATE, price_range=(100, 200))
    result = filters.to_params()
    assert result["page"] == 1
    assert result["Order"] == OrderBy.DATE
    assert result["price"] == "100-200"


def test_query_filters_to_params_with_none_values():
    filters = QueryFilters(page=None, order_by=None, price_range=None)
    result = filters.to_params()
    assert "page" in result
    assert "Order" in result
    assert "price" in result


def test_query_filters_to_clean_params():
    filters = QueryFilters(page=None, order_by=None, price_range=None)
    result = filters.to_clean_params()
    assert result == {}


def test_query_filters_iter():
    filters = QueryFilters(page=None, order_by=OrderBy.PRICE_LOWEST_TO_HIGHEST, price_range=(50, 100))
    result = dict(filters)
    assert result == {
        "Order": OrderBy.PRICE_LOWEST_TO_HIGHEST,
        "price": "50-100"
    }


@pytest.mark.parametrize(
    "input_range, expected_output",
    [
        ((1, 10), "1-10"),
        ((0, 0), "0-0"),
        ((-5, 5), "-5-5"),
        ((200, 100), "100-200"),
    ],
)
def test_format_number_range_valid(input_range, expected_output):
    assert format_number_range(input_range) == expected_output


@pytest.mark.parametrize(
    "input_range",
    [
        (None,),
        (None, 10,),
        (10, None,),
    ],
)
def test_format_number_range_invalid(input_range):
    with pytest.raises(ValueError):
        format_number_range(input_range)


def test_query_filters_immutability():
    filters = QueryFilters(page=1, order_by=OrderBy.DATE, price_range=(100, 200))
    result = filters.to_params()
    result["page"] = 2  # Modify the returned dictionary
    assert filters.page == 1  # Ensure the original object is unchanged

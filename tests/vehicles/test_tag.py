import pytest


@pytest.mark.parametrize(
    "index, expected_value",
    [
        (0, "item/8gdn3p98?opened-from=feed&component-type=main_feed&spot=standard&location=1&pagination=1"),
    ],
)
def test_relative_link(index, expected_value, cars_tags):
    assert cars_tags[index].relative_link == expected_value


@pytest.mark.parametrize(
    "index, expected_value",
    [
        (0, "https://www.yad2.co.il/vehicles/item/8gdn3p98?opened-from=feed&component-type=main_feed&spot=standard&location=1&pagination=1"),
    ],
)
def test_page_link(index, expected_value, cars_tags):
    assert cars_tags[index].page_link == expected_value


@pytest.mark.parametrize(
    "index, expected_value",
    [
        (0, "https://img.yad2.co.il/Pic/202502/09/1_3/o/y2_1pa_010861_20250209140815.jpeg?w=3840&h=3840&c=9"),
    ],
)
def test_image_url(index, expected_value, cars_tags):
    assert cars_tags[index].image_url == expected_value


@pytest.mark.parametrize(
    "index, expected_value",
    [
        (0, "ג'יפ קומפאס"),
    ],
)
def test_model(index, expected_value, cars_tags):
    assert cars_tags[index].model == expected_value


@pytest.mark.parametrize(
    "index, expected_value",
    [
        (0, "4X4 Sport פלאג-אין אוט׳ 1.3 (240 כ״ס) [2021-2025]"),
    ],
)
def test_marketing_text(index, expected_value, cars_tags):
    assert cars_tags[index].marketing_text == expected_value


@pytest.mark.parametrize(
    "index, expected_value",
    [
        (0, "2022 • יד 1"),
    ],
)
def test_year_and_hand_string(index, expected_value, cars_tags):
    assert cars_tags[index].year_and_hand_string == expected_value


@pytest.mark.parametrize(
    "index, expected_value",
    [
        (0, 2022),
    ],
)
def test_year(index, expected_value, cars_tags):
    assert cars_tags[index].year == expected_value


@pytest.mark.parametrize(
    "index, expected_value",
    [
        (0, 1),
    ],
)
def test_hand(index, expected_value, cars_tags):
    assert cars_tags[index].hand == expected_value


@pytest.mark.parametrize(
    "index, expected_value",
    [
        (0, "217,500 ₪"),
    ],
)
def test_price_string(index, expected_value, cars_tags):
    assert cars_tags[index].price_string == expected_value


@pytest.mark.parametrize(
    "index, expected_value",
    [
        (0, 217500),
    ],
)
def test_price(index, expected_value, cars_tags):
    assert cars_tags[index].price == expected_value

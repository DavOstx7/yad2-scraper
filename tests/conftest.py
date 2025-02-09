import pytest
import httpx
import respx

from yad2_scraper import Yad2Scraper


@pytest.fixture
def scraper():
    with httpx.Client() as client:
        yield Yad2Scraper(session=client)


@pytest.fixture
def mock_http():
    with respx.mock as mock:
        yield mock

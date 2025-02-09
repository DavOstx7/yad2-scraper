import pytest

from yad2_scraper.next_data import NextData


def test_next_data_initialization():
    data = {
        "props": {
            "pageProps": {
                "dehydratedState": {
                    "queries": [{"id": 1, "query": "test"}]
                }
            }
        }
    }
    next_data = NextData(data)
    assert next_data.data == data


def test_json_property():
    data = {
        "props": {
            "pageProps": {
                "dehydratedState": {
                    "queries": [{"id": 1, "query": "test"}]
                }
            }
        }
    }
    next_data = NextData(data)
    assert next_data.json == data


def test_queries_property():
    data = {
        "props": {
            "pageProps": {
                "dehydratedState": {
                    "queries": [{"id": 1, "query": "test"}]
                }
            }
        }
    }
    next_data = NextData(data)
    queries = next_data.queries
    assert isinstance(queries, list)
    assert len(queries) == 1
    assert queries[0]["id"] == 1


def test_queries_property_missing_structure():
    data = {
        "props": {
            "pageProps": {
                "dehydratedState": {}
            }
        }
    }
    next_data = NextData(data)
    with pytest.raises(KeyError):
        _ = next_data.queries


def test_getitem():
    data = {"id": 1, "text": "sample"}
    next_data = NextData(data)
    assert next_data["id"] == 1
    assert next_data["text"] == "sample"


def test_getitem_invalid_key():
    data = {"id": 1, "text": "sample"}
    next_data = NextData(data)
    with pytest.raises(KeyError):
        _ = next_data["nonexistent_key"]

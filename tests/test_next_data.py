import pytest
import random

from yad2_scraper.next_data import SafeAccessOptionalKeysMeta, NextData


def test_safe_access_optional_keys_meta_no_exceptions():
    class DummyClass(metaclass=SafeAccessOptionalKeysMeta):
        def __init__(self):
            self.data = {"key": "value"}

        @property
        def key_property(self):
            return self.data["key"]

        def key_method(self):
            return self.data["key"]

    obj = DummyClass()
    assert obj.key_property is not None
    assert obj.key_method() is not None


def test_safe_access_optional_keys_meta_catch_relevant_exceptions():
    class DummyClass(metaclass=SafeAccessOptionalKeysMeta):
        def __init__(self):
            self.data = {"key": "value"}

        def key_error(self):
            return self.data["non_existing_key"]

        def type_error(self):
            return self.data["key"]["foo"]

    obj = DummyClass()
    assert obj.key_error() is None
    assert obj.type_error() is None


def test_safe_access_optional_keys_meta_not_catch_other_exceptions():
    class DummyClass(metaclass=SafeAccessOptionalKeysMeta):
        def __init__(self):
            self.data = {"not_a_dict": "value"}

        def random_error(self):
            raise random.choice([AttributeError, IndexError, ValueError])

    obj = DummyClass()
    with pytest.raises(Exception):
        obj.random_error()


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

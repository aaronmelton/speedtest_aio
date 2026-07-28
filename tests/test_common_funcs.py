"""Unit tests for common_funcs.pretty_print."""

import json

import pytest

from speedtest_aio.common_funcs import pretty_print


def test_pretty_print_formats_dict_with_indentation() -> None:
    """A dict is rendered as indented JSON."""
    result = pretty_print({"a": 1, "b": 2})
    assert json.loads(result) == {"a": 1, "b": 2}
    assert "\n" in result


def test_pretty_print_formats_list() -> None:
    """A list is rendered as indented JSON."""
    result = pretty_print([1, 2, 3])
    assert json.loads(result) == [1, 2, 3]


def test_pretty_print_formats_nested_structures() -> None:
    """Nested dicts/lists are rendered correctly."""
    nested_obj = {"outer": {"inner": [1, 2, {"deep": "value"}]}}
    result = pretty_print(nested_obj)
    assert json.loads(result) == nested_obj


def test_pretty_print_formats_empty_dict() -> None:
    """An empty dict renders as an empty JSON object."""
    assert pretty_print({}) == "{}"


def test_pretty_print_formats_empty_list() -> None:
    """An empty list renders as an empty JSON array."""
    assert pretty_print([]) == "[]"


def test_pretty_print_serializes_object_with_to_dict_method() -> None:
    """An object exposing to_dict() is serialized via that method."""

    class Widget:
        """Minimal stand-in for a class-based result object."""

        def to_dict(self) -> dict:
            """Return the dict representation used for serialization."""
            return {"name": "widget"}

    result = pretty_print(Widget())
    assert json.loads(result) == {"name": "widget"}


def test_pretty_print_raises_type_error_for_non_serializable_object() -> None:
    """An object without to_dict() and not JSON-serializable raises TypeError."""

    class Unserializable:
        """Object with no to_dict() method and no JSON support."""

    with pytest.raises(TypeError, match="not JSON serializable"):
        pretty_print(Unserializable())

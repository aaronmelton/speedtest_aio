"""Aaron's Common Functions."""

from json import dumps as json_dumps
from typing import Any


def pretty_print(this_obj: Any) -> str:
    """Return a nicely-formatted JSON string, with support for class objects.

    Args:
        this_obj (any): The object (dict, list, or class instance) to be converted to a pretty-printed JSON string.

    Returns:
        str: A JSON-formatted string with indentation for readability.
    """

    def class_to_dict(obj: Any) -> Any:
        """Custom serializer function to handle class objects."""
        # If the object has a `to_dict()` method, use it to convert to a dictionary
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        # Otherwise, raise a TypeError to let JSON know it's not serializable
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    return json_dumps(this_obj, indent=4, default=class_to_dict)

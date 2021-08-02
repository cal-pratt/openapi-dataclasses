from dataclasses import dataclass
from typing import Optional


@dataclass
class PythonEnumAttribute:
    attribute_name: str
    """
    The name of the attribute
    """

    attribute_value: str
    """
    The value for the attribute
    """


@dataclass
class PythonClassAttribute:
    attribute_name: str
    """
    The name of the attribute
    """

    openapi_name: str
    """
    The name of the attribute as defined in the openapi.json
    """

    attribute_type: str
    """
    The type for the attribute
    """

    attribute_default: Optional[str]
    """
    The default value of the attribute
    """

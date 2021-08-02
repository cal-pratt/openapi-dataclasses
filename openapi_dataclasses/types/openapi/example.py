from dataclasses import dataclass
from typing import Optional, Any

from dataclasses_json import dataclass_json, CatchAll, Undefined

from .field import openapi_field


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OpenApiExample:
    """
    The example value is expected to be compatible with the type schema of its associated value.
    Tooling implementations MAY choose to validate compatibility automatically, and reject the
    example value(s) if incompatible.
    """

    summary: Optional[str] = openapi_field("summary", default=None)
    """
    Short description for the example.
    """

    description: Optional[str] = openapi_field("description", default=None)
    """
    Long description for the example. CommonMark syntax MAY be used for rich text representation.
    """

    value: Any = openapi_field("value", default=None)
    """
    Embedded literal example. The value field and externalValue field are mutually exclusive. 
    To represent examples of media types that cannot naturally represented in JSON or YAML, use a 
    string value to contain the example, escaping where necessary.
    """

    external_value: Optional[str] = openapi_field("externalValue", default=None)
    """
    A URL that points to the literal example. This provides the capability to reference examples 
    that cannot easily be included in JSON or YAML documents. The value field and externalValue 
    field are mutually exclusive.
    """

    unhandled_data: CatchAll = openapi_field(default_factory=dict)

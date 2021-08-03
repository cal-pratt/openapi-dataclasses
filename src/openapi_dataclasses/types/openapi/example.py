from dataclasses import dataclass, field
from typing import Any, Optional

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config


@dataclass
class OpenApiExample(DataClassJsonMixin):
    """
    The example value is expected to be compatible with the type schema of its associated value.
    Tooling implementations MAY choose to validate compatibility automatically, and reject the
    example value(s) if incompatible.
    """

    summary: Optional[str] = None
    """
    Short description for the example.
    """

    description: Optional[str] = None
    """
    Long description for the example. CommonMark syntax MAY be used for rich text representation.
    """

    value: Any = None
    """
    Embedded literal example. The value field and externalValue field are mutually exclusive.
    To represent examples of media types that cannot naturally represented in JSON or YAML, use a
    string value to contain the example, escaping where necessary.
    """

    external_value: Optional[str] = None
    """
    A URL that points to the literal example. This provides the capability to reference examples
    that cannot easily be included in JSON or YAML documents. The value field and externalValue
    field are mutually exclusive.
    """

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

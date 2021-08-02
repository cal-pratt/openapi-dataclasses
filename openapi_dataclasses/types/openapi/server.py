from dataclasses import dataclass
from typing import Optional, Any

from dataclasses_json import dataclass_json, CatchAll, Undefined

from .field import openapi_field


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OpenApiServerVariable:
    """
    An object representing a Server Variable for server URL template substitution.
    """

    default: str = openapi_field("description")
    """
    The default value to use for substitution, which SHALL be sent if an alternate value is not 
    supplied. Note this behavior is different than the Schema Object's treatment of default values, 
    because in those cases parameter values are optional. If the enum is defined, the value SHOULD 
    exist in the enum's values.
    """

    enum: list[str] = openapi_field("enum", default_factory=list)
    """
    An enumeration of string values to be used if the substitution options are from a limited set. 
    The array SHOULD NOT be empty.
    """

    description: Optional[str] = openapi_field("description", default=None)
    """
    An optional description for the server variable. CommonMark syntax MAY be used for rich text 
    representation.
    """

    unhandled_data: CatchAll = openapi_field(default_factory=dict)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OpenApiServer:
    """
    An object representing a Server.
    """

    url: str = openapi_field("url")
    """
    A URL to the target host. This URL supports Server Variables and MAY be relative, to indicate 
    that the host location is relative to the location where the OpenAPI document is being served. 
    Variable substitutions will be made when a variable is named in {brackets}.
    """

    description: Optional[str] = openapi_field("description", default=None)
    """
    An optional string describing the host designated by the URL. CommonMark syntax MAY be used for 
    rich text representation.
    """

    variables: dict[str, OpenApiServerVariable] = openapi_field("variables", default_factory={})
    """
    A map between a variable name and its value. The value is used for substitution in the server's 
    URL template.
    """

    unhandled_data: CatchAll = openapi_field(default_factory=dict)

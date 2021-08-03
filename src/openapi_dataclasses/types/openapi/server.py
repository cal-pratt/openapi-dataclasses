from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config


@dataclass
class OpenApiServerVariable(DataClassJsonMixin):
    """
    An object representing a Server Variable for server URL template substitution.
    """

    default: str
    """
    The default value to use for substitution, which SHALL be sent if an alternate value is not
    supplied. Note this behavior is different than the Schema Object's treatment of default values,
    because in those cases parameter values are optional. If the enum is defined, the value SHOULD
    exist in the enum's values.
    """

    enum: list[str] = field(default_factory=list)
    """
    An enumeration of string values to be used if the substitution options are from a limited set.
    The array SHOULD NOT be empty.
    """

    description: Optional[str] = None
    """
    An optional description for the server variable. CommonMark syntax MAY be used for rich text
    representation.
    """

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)


@dataclass
class OpenApiServer(DataClassJsonMixin):
    """
    An object representing a Server.
    """

    url: str
    """
    A URL to the target host. This URL supports Server Variables and MAY be relative, to indicate
    that the host location is relative to the location where the OpenAPI document is being served.
    Variable substitutions will be made when a variable is named in {brackets}.
    """

    description: Optional[str] = field(default=None)
    """
    An optional string describing the host designated by the URL. CommonMark syntax MAY be used for
    rich text representation.
    """

    variables: dict[str, OpenApiServerVariable] = field(default_factory=dict)
    """
    A map between a variable name and its value. The value is used for substitution in the server's
    URL template.
    """

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

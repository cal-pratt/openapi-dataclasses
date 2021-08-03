from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config


@dataclass
class OpenApiExternalDocumentation(DataClassJsonMixin):
    """
    Allows referencing an external resource for extended documentation.
    """

    url: str
    """
    The URL for the target documentation. Value MUST be in the format of a URL.
    """

    description: Optional[str] = None
    """
    A short description for the tag. CommonMark syntax MAY be used for rich text representation.
    """

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

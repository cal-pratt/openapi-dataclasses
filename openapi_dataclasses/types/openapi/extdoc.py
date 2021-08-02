from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json, CatchAll, Undefined

from .field import openapi_field


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OpenApiExternalDocumentation:
    """
    Allows referencing an external resource for extended documentation.
    """

    url: str = openapi_field("url")
    """
    The URL for the target documentation. Value MUST be in the format of a URL.
    """

    description: Optional[str] = openapi_field("description", default=None)
    """
    A short description for the tag. CommonMark syntax MAY be used for rich text representation.
    """

    unhandled_data: CatchAll = openapi_field(default_factory=dict)

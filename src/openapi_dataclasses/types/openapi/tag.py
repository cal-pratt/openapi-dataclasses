from dataclasses import dataclass, field
from typing import Optional

from ...meta import metadata
from .extdoc import OpenApiExternalDocumentation


@dataclass
class OpenApiTag:
    """
    Adds metadata to a single tag that is used by the Operation Object. It is not mandatory to have
    a Tag Object per tag defined in the Operation Object instances.
    """

    name: str
    """
    The name of the tag.
    """

    description: Optional[str] = None
    """
    A short description for the tag. CommonMark syntax MAY be used for rich text representation.
    """

    external_docs: Optional[OpenApiExternalDocumentation] = field(
        metadata=metadata(name="externalDocs"), default=None
    )
    """
    Additional external documentation for this tag.
    """

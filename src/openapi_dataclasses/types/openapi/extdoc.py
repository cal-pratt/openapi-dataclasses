from dataclasses import dataclass
from typing import Optional


@dataclass
class OpenApiExternalDocumentation:
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

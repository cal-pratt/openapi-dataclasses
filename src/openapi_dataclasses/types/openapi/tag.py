from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config

from .extdoc import OpenApiExternalDocumentation


@dataclass
class OpenApiTag(DataClassJsonMixin):
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
        metadata=config(field_name="externalDocs"), default=None
    )
    """
    Additional external documentation for this tag.
    """

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config


@dataclass
class OpenApiContact(DataClassJsonMixin):
    """
    Contact information for the exposed API.
    """

    name: Optional[str] = None
    """
    The identifying name of the contact person/organization.
    """

    url: Optional[str] = None
    """
    The URL pointing to the contact information. MUST be in the format of a URL.
    """

    email: Optional[str] = None
    """
    The email address of the contact person/organization. MUST be in the format of an email address.
    """

    unhandled_data: CatchAll = field(default_factory=dict)


@dataclass
class OpenApiInfo(DataClassJsonMixin):
    """
    The object provides metadata about the API. The metadata MAY be used by the clients if needed,
    and MAY be presented in editing or documentation generation tools for convenience.
    """

    version: str
    """
    The version of the OpenAPI document 
    (which is distinct from the OpenAPI Specification version or the API implementation version).
    """

    title: str = ""
    """
    The title of the API.
    """

    description: Optional[str] = None
    """
    A short description of the API. CommonMark syntax MAY be used for rich text representation.
    """

    terms_of_service: Optional[str] = field(
        metadata=config(field_name="termsOfService"), default=None
    )
    """
    A URL to the Terms of Service for the API. MUST be in the format of a URL.
    """

    contact: Optional[OpenApiContact] = None
    """
    The contact information for the exposed API.
    """

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

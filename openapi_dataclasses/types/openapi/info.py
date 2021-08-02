from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json, Undefined, CatchAll

from .field import openapi_field


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OpenApiContact:
    """
    Contact information for the exposed API.
    """

    name: Optional[str] = openapi_field("name", default=None)
    """
    The identifying name of the contact person/organization.
    """

    url: Optional[str] = openapi_field("url", default=None)
    """
    The URL pointing to the contact information. MUST be in the format of a URL.
    """

    email: Optional[str] = openapi_field("email", default=None)
    """
    The email address of the contact person/organization. MUST be in the format of an email address.
    """


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OpenApiInfo:
    """
    The object provides metadata about the API. The metadata MAY be used by the clients if needed,
    and MAY be presented in editing or documentation generation tools for convenience.
    """

    version: str = openapi_field("version")
    """
    The version of the OpenAPI document 
    (which is distinct from the OpenAPI Specification version or the API implementation version).
    """

    title: str = openapi_field("title", default='')
    """
    The title of the API.
    """

    description: Optional[str] = openapi_field("title", default=None)
    """
    A short description of the API. CommonMark syntax MAY be used for rich text representation.
    """

    terms_of_service: Optional[str] = openapi_field("termsOfService", default=None)
    """
    A URL to the Terms of Service for the API. MUST be in the format of a URL.
    """

    contact: Optional[OpenApiContact] = openapi_field("termsOfService", default=None)
    """
    The contact information for the exposed API.
    """

    unhandled_data: CatchAll = openapi_field(default_factory=dict)

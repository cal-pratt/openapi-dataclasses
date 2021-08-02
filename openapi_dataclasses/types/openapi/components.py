from dataclasses import dataclass

from dataclasses_json import dataclass_json, CatchAll, Undefined

from .example import OpenApiExample
from .header import OpenApiHeader
from .link import OpenApiLink
from .parameter import OpenApiParameter
from .path import OpenApiPath
from .requestbody import OpenApiRequestBody
from .response import OpenApiResponse
from .schema import OpenApiSchema
from .field import openapi_field
from .securityscheme import OpenApiSecurityScheme


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OpenApiComponents:
    """
    Holds a set of reusable objects for different aspects of the OAS. All objects defined within
    the components object will have no effect on the API unless they are explicitly referenced from
    properties outside the components object.
    """

    schemas: dict[str, OpenApiSchema] = openapi_field("schemas", default_factory=dict)

    responses: dict[str, OpenApiResponse] = openapi_field("responses", default_factory=dict)

    parameters: dict[str, OpenApiParameter] = openapi_field("parameters", default_factory=dict)

    examples: dict[str, OpenApiExample] = openapi_field("examples", default_factory=dict)

    request_bodies: dict[str, OpenApiRequestBody] = openapi_field("requestBodies", default_factory=dict)

    headers: dict[str, OpenApiHeader] = openapi_field("headers", default_factory=dict)

    security_schemes: dict[str, OpenApiSecurityScheme] = openapi_field("securitySchemes", default_factory=dict)

    links: dict[str, OpenApiLink] = openapi_field("links", default_factory=dict)

    callbacks: dict[str, OpenApiPath] = openapi_field("callbacks", default_factory=dict)
    """
    A map of possible out-of band callbacks related to the parent operation. Each value in the map
    is a Path Item Object that describes a set of requests that may be initiated by the API 
    provider and the expected responses. The key value used to identify the path item object is an 
    expression,evaluated at runtime, that identifies a URL to use for the callback operation.
    """

    unhandled_data: CatchAll = openapi_field(default_factory=dict)

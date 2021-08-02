from dataclasses import dataclass

from dataclasses_json import dataclass_json, CatchAll, Undefined

from .field import openapi_field


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OpenApiSecurityScheme:
    """
    Defines a security scheme that can be used by the operations. Supported schemes are HTTP
    authentication, an API key (either as a header, a cookie parameter or as a query parameter),
    OAuth2's common flows (implicit, password, client credentials and authorization code) as
    defined in RFC6749, and OpenID Connect Discovery.
    """

    unhandled_data: CatchAll = openapi_field(default_factory=dict)

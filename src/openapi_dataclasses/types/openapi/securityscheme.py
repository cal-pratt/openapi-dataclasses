from dataclasses import dataclass


@dataclass
class OpenApiSecurityScheme:
    """
    Defines a security scheme that can be used by the operations. Supported schemes are HTTP
    authentication, an API key (either as a header, a cookie parameter or as a query parameter),
    OAuth2's common flows (implicit, password, client credentials and authorization code) as
    defined in RFC6749, and OpenID Connect Discovery.
    """

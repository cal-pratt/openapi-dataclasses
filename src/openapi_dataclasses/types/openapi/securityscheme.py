from dataclasses import dataclass, field

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config


@dataclass
class OpenApiSecurityScheme(DataClassJsonMixin):
    """
    Defines a security scheme that can be used by the operations. Supported schemes are HTTP
    authentication, an API key (either as a header, a cookie parameter or as a query parameter),
    OAuth2's common flows (implicit, password, client credentials and authorization code) as
    defined in RFC6749, and OpenID Connect Discovery.
    """

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

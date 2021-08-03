from dataclasses import dataclass, field

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config

from .components import OpenApiComponents
from .info import OpenApiInfo
from .path import OpenApiPath
from .server import OpenApiServer
from .tag import OpenApiTag


@dataclass
class OpenApiSpec(DataClassJsonMixin):
    """
    This is the root document object of the OpenAPI document.
    """

    openapi: str
    """
    This string MUST be the semantic version number of the OpenAPI Specification version that the
    OpenAPI document uses. The openapi field SHOULD be used by tooling specifications and clients to
    interpret the OpenAPI document. This is not related to the API info.version string.
    """

    info: OpenApiInfo
    """
    Provides metadata about the API. The metadata MAY be used by tooling as required.
    """

    paths: dict[str, OpenApiPath]
    """
    The available paths and operations for the API.
    """

    servers: list[OpenApiServer] = field(default_factory=list)
    """
    An array of Server Objects, which provide connectivity information to a target server. If the
    servers property is not provided, or is an empty array, the default value would be a Server
    Object with a url value of /.
    """

    components: OpenApiComponents = field(default_factory=OpenApiComponents)
    """
    An element to hold various schemas for the specification.
    """

    security: list[dict[str, list[str]]] = field(default_factory=list)
    """
    A declaration of which security mechanisms can be used across the API. The list of values
    includes alternative security requirement objects that can be used. Only one of the security
    requirement objects need to be satisfied to authorize a request. Individual operations can
    override this definition. To make security optional, an empty security requirement ({}) can be
    included in the array.

    Each name MUST correspond to a security scheme which is declared in the Security Schemes under
    the Components Object. If the security scheme is of type "oauth2" or "openIdConnect", then the
    value is a list of scope names required for the execution, and the list MAY be empty if
    authorization does not require a specified scope. For other security scheme types, the array
    MUST be empty.
    """

    tags: list[OpenApiTag] = field(default_factory=list)

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

    @classmethod
    def load(cls, filename: str) -> "OpenApiSpec":
        with open(filename, "rb") as openapi_json:
            return OpenApiSpec.from_json(openapi_json.read())

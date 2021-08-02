from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json, CatchAll, Undefined

from .parameter import OpenApiParameter
from .server import OpenApiServer
from .operation import OpenApiOperation
from .field import openapi_field


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OpenApiPath:
    """
    Describes the operations available on a single path. A Path Item MAY be empty, due to ACL
    constraints. The path itself is still exposed to the documentation viewer but they will not
    know which operations and parameters are available.
    """

    ref: Optional[str] = openapi_field("$ref", default=None)
    """
    Allows for an external definition of this path item. The referenced structure MUST be in the 
    format of a Path Item Object. In case a Path Item Object field appears both in the defined 
    object and the referenced object, the behavior is undefined.
    """

    summary: Optional[str] = openapi_field("summary", default=None)
    """
    An optional, string summary, intended to apply to all operations in this path.
    """

    description: Optional[str] = openapi_field("description", default=None)
    """
    An optional, string description, intended to apply to all operations in this path. 
    CommonMark syntax MAY be used for rich text representation.
    """

    get: Optional[OpenApiOperation] = openapi_field("get", default=None)
    """
    A definition of a GET operation on this path.
    """

    put: Optional[OpenApiOperation] = openapi_field("put", default=None)
    """
    A definition of a PUT operation on this path.
    """

    post: Optional[OpenApiOperation] = openapi_field("post", default=None)
    """
    A definition of a POST operation on this path.
    """

    delete: Optional[OpenApiOperation] = openapi_field("delete", default=None)
    """
    A definition of a DELETE operation on this path.
    """

    options: Optional[OpenApiOperation] = openapi_field("options", default=None)
    """
    A definition of a OPTIONS operation on this path.
    """

    head: Optional[OpenApiOperation] = openapi_field("head", default=None)
    """
    A definition of a HEAD operation on this path.
    """

    patch: Optional[OpenApiOperation] = openapi_field("patch", default=None)
    """
    A definition of a PATCH operation on this path.
    """

    trace: Optional[OpenApiOperation] = openapi_field("trace", default=None)
    """
    A definition of a TRACE operation on this path.
    """

    servers: list[OpenApiServer] = openapi_field("servers", default_factory=list)
    """
    An alternative server array to service all operations in this path.
    """

    parameters: dict[str, OpenApiParameter] = openapi_field("parameters", default_factory=dict)
    """
    A list of parameters that are applicable for all the operations described under this path. 
    These parameters can be overridden at the operation level, but cannot be removed there. 
    The list MUST NOT include duplicated parameters. A unique parameter is defined by a combination 
    of a name and location. The list can use the Reference Object to link to parameters that are 
    defined at the OpenAPI Object's components/parameters.
    """

    unhandled_data: CatchAll = openapi_field(default_factory=dict)

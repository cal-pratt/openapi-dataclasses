from dataclasses import dataclass, field
from typing import Optional

from ...meta import metadata
from .operation import OpenApiOperation
from .parameter import OpenApiParameter
from .server import OpenApiServer


@dataclass
class OpenApiPath:
    """
    Describes the operations available on a single path. A Path Item MAY be empty, due to ACL
    constraints. The path itself is still exposed to the documentation viewer but they will not
    know which operations and parameters are available.
    """

    ref: Optional[str] = field(metadata=metadata(name="$ref"), default=None)
    """
    Allows for an external definition of this path item. The referenced structure MUST be in the
    format of a Path Item Object. In case a Path Item Object field appears both in the defined
    object and the referenced object, the behavior is undefined.
    """

    summary: Optional[str] = None
    """
    An optional, string summary, intended to apply to all operations in this path.
    """

    description: Optional[str] = None
    """
    An optional, string description, intended to apply to all operations in this path.
    CommonMark syntax MAY be used for rich text representation.
    """

    get: Optional[OpenApiOperation] = None
    """
    A definition of a GET operation on this path.
    """

    put: Optional[OpenApiOperation] = None
    """
    A definition of a PUT operation on this path.
    """

    post: Optional[OpenApiOperation] = None
    """
    A definition of a POST operation on this path.
    """

    delete: Optional[OpenApiOperation] = None
    """
    A definition of a DELETE operation on this path.
    """

    options: Optional[OpenApiOperation] = None
    """
    A definition of a OPTIONS operation on this path.
    """

    head: Optional[OpenApiOperation] = None
    """
    A definition of a HEAD operation on this path.
    """

    patch: Optional[OpenApiOperation] = None
    """
    A definition of a PATCH operation on this path.
    """

    trace: Optional[OpenApiOperation] = None
    """
    A definition of a TRACE operation on this path.
    """

    servers: list[OpenApiServer] = field(default_factory=list)
    """
    An alternative server array to service all operations in this path.
    """

    parameters: dict[str, OpenApiParameter] = field(default_factory=dict)
    """
    A list of parameters that are applicable for all the operations described under this path.
    These parameters can be overridden at the operation level, but cannot be removed there.
    The list MUST NOT include duplicated parameters. A unique parameter is defined by a combination
    of a name and location. The list can use the Reference Object to link to parameters that are
    defined at the OpenAPI Object's components/parameters.
    """

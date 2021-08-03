"""
The classes modeled in this module were sourced from the documentation available at
https://swagger.io/specification/
"""

from .components import OpenApiComponents
from .example import OpenApiExample
from .extdoc import OpenApiExternalDocumentation
from .header import OpenApiHeader
from .info import OpenApiContact, OpenApiInfo
from .link import OpenApiLink
from .operation import OpenApiOperation
from .parameter import OpenApiParameter
from .path import OpenApiPath
from .requestbody import OpenApiRequestBody
from .response import OpenApiResponse
from .schema import OpenApiSchema
from .securityscheme import OpenApiSecurityScheme
from .server import OpenApiServer, OpenApiServerVariable
from .spec import OpenApiSpec
from .tag import OpenApiExternalDocumentation, OpenApiTag

__all__ = [
    "OpenApiContact",
    "OpenApiInfo",
    "OpenApiSchema",
    "OpenApiExample",
    "OpenApiHeader",
    "OpenApiServer",
    "OpenApiServerVariable",
    "OpenApiLink",
    "OpenApiParameter",
    "OpenApiPath",
    "OpenApiRequestBody",
    "OpenApiResponse",
    "OpenApiSecurityScheme",
    "OpenApiExternalDocumentation",
    "OpenApiTag",
    "OpenApiComponents",
    "OpenApiSpec",
    "OpenApiOperation",
    "OpenApiExternalDocumentation",
]

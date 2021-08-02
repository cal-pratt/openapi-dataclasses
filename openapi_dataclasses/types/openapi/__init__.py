"""
The classes modeled in this module were sourced from the documentation available at
https://swagger.io/specification/
"""

from .info import OpenApiContact, OpenApiInfo
from .schema import OpenApiSchema
from .example import OpenApiExample
from .header import OpenApiHeader
from .server import OpenApiServer, OpenApiServerVariable
from .link import OpenApiLink
from .parameter import OpenApiParameter
from .path import OpenApiPath
from .requestbody import OpenApiRequestBody
from .response import OpenApiResponse
from .securityscheme import OpenApiSecurityScheme
from .tag import OpenApiExternalDocumentation, OpenApiTag
from .components import OpenApiComponents
from .spec import OpenApiSpec

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
]

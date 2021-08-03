from dataclasses import dataclass, field
from typing import Any, ClassVar

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config

from .example import OpenApiExample
from .header import OpenApiHeader
from .link import OpenApiLink
from .parameter import OpenApiParameter
from .requestbody import OpenApiRequestBody
from .response import OpenApiResponse
from .schema import OpenApiSchema
from .securityscheme import OpenApiSecurityScheme


@dataclass
class OpenApiComponents(DataClassJsonMixin):
    """
    Holds a set of reusable objects for different aspects of the OAS. All objects defined within
    the components object will have no effect on the API unless they are explicitly referenced from
    properties outside the components object.
    """

    schemas: dict[str, OpenApiSchema] = field(default_factory=dict)

    responses: dict[str, OpenApiResponse] = field(default_factory=dict)

    parameters: dict[str, OpenApiParameter] = field(default_factory=dict)

    examples: dict[str, OpenApiExample] = field(default_factory=dict)

    request_bodies: dict[str, OpenApiRequestBody] = field(
        metadata=config(field_name="requestBodies"), default_factory=dict
    )

    headers: dict[str, OpenApiHeader] = field(default_factory=dict)

    security_schemes: dict[str, OpenApiSecurityScheme] = field(
        metadata=config(field_name="securitySchemes"), default_factory=dict
    )

    links: dict[str, OpenApiLink] = field(default_factory=dict)

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

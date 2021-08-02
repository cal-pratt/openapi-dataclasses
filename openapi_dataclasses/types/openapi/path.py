from dataclasses import dataclass

from dataclasses_json import dataclass_json, CatchAll, Undefined

from .field import openapi_field


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OpenApiPath:
    """
    Describes the operations available on a single path. A Path Item MAY be empty, due to ACL
    constraints. The path itself is still exposed to the documentation viewer but they will not
    know which operations and parameters are available.
    """

    unhandled_data: CatchAll = openapi_field(default_factory=dict)

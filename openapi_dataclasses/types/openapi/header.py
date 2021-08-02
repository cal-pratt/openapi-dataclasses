from dataclasses import dataclass

from dataclasses_json import dataclass_json, CatchAll, Undefined

from .field import openapi_field


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OpenApiHeader:
    """
    The Header Object follows the structure of the Parameter Object with the following changes:

        1. name MUST NOT be specified, it is given in the corresponding headers map.

        2. in MUST NOT be specified, it is implicitly in header.

        3. All traits that are affected by the location MUST be applicable to a location of header
            (for example, style).
    """

    unhandled_data: CatchAll = openapi_field(default_factory=dict)

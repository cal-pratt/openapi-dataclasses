from dataclasses import dataclass, field

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config


@dataclass
class OpenApiHeader(DataClassJsonMixin):
    """
    The Header Object follows the structure of the Parameter Object with the following changes:

        1. name MUST NOT be specified, it is given in the corresponding headers map.

        2. in MUST NOT be specified, it is implicitly in header.

        3. All traits that are affected by the location MUST be applicable to a location of header
            (for example, style).
    """

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

from dataclasses import dataclass, field
from typing import Any, ClassVar

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config


@dataclass
class OpenApiRequestBody(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

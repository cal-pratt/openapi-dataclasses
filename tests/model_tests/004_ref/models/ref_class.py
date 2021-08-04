from dataclasses import dataclass, field

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config

from .enum_class import EnumClass


@dataclass
class RefClass(DataClassJsonMixin):
    reference: EnumClass = field(metadata=config(field_name="reference"))

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

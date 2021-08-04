from dataclasses import dataclass, field

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config


@dataclass
class ClassSchema(DataClassJsonMixin):
    one: int = field(metadata=config(field_name="one"))
    two: float = field(metadata=config(field_name="two"))
    three: str = field(metadata=config(field_name="three"))

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

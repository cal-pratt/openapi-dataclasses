from dataclasses import dataclass, field

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config


@dataclass
class SomeComplexSchemaName(DataClassJsonMixin):
    one: int = field(metadata=config(field_name="One"))
    two_two: float = field(metadata=config(field_name="two_Two"))
    three_three: str = field(metadata=config(field_name="THREE-three"))

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

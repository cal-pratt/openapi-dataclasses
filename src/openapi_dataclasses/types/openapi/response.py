from dataclasses import dataclass, field

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config


@dataclass
class OpenApiResponse(DataClassJsonMixin):
    """
    Describes a single response from an API Operation, including design-time, static links to
    operations based on the response.
    """

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

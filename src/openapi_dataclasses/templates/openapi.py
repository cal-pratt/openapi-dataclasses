import dataclasses
from typing import Any, Callable, Optional

import dataclasses_json


def openapi_field(
    property_name: Optional[str] = None,
    *,
    default: Any = None,
    default_factory: Any = dataclasses.MISSING,
    decoder: Callable[[Any], Any] = None
) -> dataclasses.Field:
    return dataclasses.field(
        metadata=dataclasses_json.config(
            field_name=property_name if property_name else None,
            decoder=decoder if decoder else None,
        ),
        default=default,
        default_factory=default_factory,
    )


def openapi_unhandled() -> dataclasses.Field:
    return dataclasses.field(default_factory=dict)

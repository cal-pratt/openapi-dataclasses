import dataclasses
from typing import Any, Optional, Callable

import dataclasses_json


def openapi_field(
    property_name: Optional[str] = None,
    *,
    default: Any = dataclasses.MISSING,
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

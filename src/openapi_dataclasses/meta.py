from collections.abc import Callable
from typing import Any, Optional


def metadata(
    *,
    name: Optional[str] = None,
    decoder: Optional[Callable[[Any], Any]] = None,
) -> dict[str, dict[str, Any]]:
    openapi_metadata: dict[str, Any] = {}
    if name:
        openapi_metadata["name"] = name
    if decoder:
        openapi_metadata["decoder"] = decoder
    return dict(openapi_dataclasses=openapi_metadata)

from typing import Any, Type

from .handler import DecoderHandler, HandlerResponse


class NoneHandler(DecoderHandler):
    def decode(self, clazz: Type[Any], data: Any) -> HandlerResponse:
        if data is not None:
            raise ValueError
        return None  # type: ignore

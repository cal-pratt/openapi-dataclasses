from typing import Any, Type

from .handler import DecoderHandler, HandlerResponse


class AnyHandler(DecoderHandler):
    def decode(self, clazz: Type[Any], data: Any) -> HandlerResponse:
        """
        The simplest form. We can assume that we can just return whatever data is provided.
        """

        return data

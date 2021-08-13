from typing import Any, Type

from .handler import DecoderHandler, HandlerResponse


class ClassHandler(DecoderHandler):
    def decode(self, clazz: Type[Any], data: Any) -> HandlerResponse:
        """
        This method will get hit by most of the primitive values. The class is used to instantiate
        the value to the correct type to avoid type inconsistency (say between int and float).
        """

        return clazz(data)

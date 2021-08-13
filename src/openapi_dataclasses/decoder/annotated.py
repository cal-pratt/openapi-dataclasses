from typing import Any, Type

from .handler import DecoderHandler, HandlerResponse
from .util import get_cached_class_args


class AnnotatedHandler(DecoderHandler):
    def decode(self, clazz: Type[Any], data: Any) -> HandlerResponse:
        """
        The simplest form. We can assume that we can just return whatever data is provided.
        """
        _, clazz_args = get_cached_class_args(clazz)

        if len(clazz_args) == 0:
            clazz_args = [Any]  # type: ignore

        return (yield clazz_args[0], data)

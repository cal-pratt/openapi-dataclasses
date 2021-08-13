from collections.abc import Sequence
from typing import Any, Type

from .handler import DecoderHandler, HandlerResponse
from .util import get_cached_class_args


class IterHandler(DecoderHandler):
    def decode(self, clazz: Type[Any], data: Any) -> HandlerResponse:
        clazz_origin, clazz_args = get_cached_class_args(clazz)

        if clazz_origin is Sequence:
            clazz_origin = list

        """
        This is a helper method for all of the iterable types. We can create a generator
        and provide that to the constructor of the different list types.
        """

        if len(clazz_args) == 0:
            clazz_args = [Any]  # type: ignore
        elif len(clazz_args) != 1:
            raise ValueError

        response = []
        for element in data:
            response.append((yield clazz_args[0], element))
        return clazz_origin(response)

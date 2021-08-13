from typing import Any, Iterable, Type

from .handler import DecoderHandler, HandlerResponse
from .util import get_cached_class_args


class DictHandler(DecoderHandler):
    def decode(self, clazz: Type[Any], data: Any) -> HandlerResponse:
        _, clazz_args = get_cached_class_args(clazz)

        if len(clazz_args) == 0:
            clazz_args = [Any, Any]  # type: ignore
        elif len(clazz_args) != 2:
            raise ValueError

        if isinstance(data, dict):
            stream = ((key, val) for key, val in data.items())
        elif isinstance(data, Iterable):
            stream = ((key, val) for key, val in data)
        else:
            raise ValueError

        response = {}
        for key, val in stream:
            key_data = (yield clazz_args[0], key)
            val_data = (yield clazz_args[1], val)
            response[key_data] = val_data
        return response

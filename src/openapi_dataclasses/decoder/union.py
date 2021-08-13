from collections.abc import Sequence
from typing import Any, Type

from .handler import DecoderHandler, HandlerResponse
from .util import get_cached_class_args

COMMON_TYPES = (
    type(None),
    int,
    float,
    bool,
    str,
    list,
    tuple,
    set,
    frozenset,
    Sequence,
)


class UnionHandler(DecoderHandler):
    def decode(self, clazz: Type[Any], data: Any) -> HandlerResponse:
        """
        Decodes the class into the appropriate class in the union. If the union types any basic
        types, then we'll short circuit and try them directly. If the class is complex (i.e more
        than one dataclass in the union) then we'll just attempt a conversion to each one in order.

        TODO: for an optimal choice this decoder can be enhanced to check field-names in dicts.
        """

        _, clazz_args = get_cached_class_args(clazz)

        if len(clazz_args) == 0:
            clazz_args = [Any]  # type: ignore

        # First see if we directly match any simple types.
        # Also we can filter out all of the simple types.
        filtered_clazz_args: list[Type[Any]] = []

        for clazz_arg in clazz_args:
            clazz_origin, _ = get_cached_class_args(clazz_arg)
            if clazz_origin in COMMON_TYPES:
                if isinstance(data, clazz_origin):
                    return (yield clazz_arg, data)
            else:
                filtered_clazz_args.append(clazz_arg)

        # If there's only one choice after filtering, lets just return it.
        if len(filtered_clazz_args) == 1:
            return (yield filtered_clazz_args[0], data)

        # Try all of the remaining types one at a time.
        # We can possibly do better by examining fields.
        for clazz_arg in filtered_clazz_args:
            try:
                return (yield clazz_arg, data)
            except:  # noqa: E722
                pass

        # We didn't find anything, lets just give up.
        raise ValueError

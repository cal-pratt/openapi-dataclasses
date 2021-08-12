from typing import Any

from .handler import Clazz, ClazzArgs, Data, DecoderHandler, Obj
from .util import examine_class

COMMON_TYPES = (type(None), int, float, bool, str, list)


class UnionHandler(DecoderHandler):
    def decode(
        self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data
    ) -> Obj:
        if len(clazz_args) == 0:
            clazz_args = [Any]  # type: ignore

        # First see if we directly match any simple types.
        # Also we can filter out all of the simple types.
        filtered_clazz_args: list[Clazz] = []

        for clazz_arg in clazz_args:
            optional_clazz, optional_clazz_args = examine_class(clazz_arg)
            if optional_clazz in COMMON_TYPES:
                if isinstance(data, optional_clazz):
                    return root.decode(root, optional_clazz, optional_clazz_args, data)
            else:
                filtered_clazz_args.append(clazz_arg)

        # If there's only one choice after filtering, lets just return it.
        if len(clazz_args) == 1:
            optional_clazz, optional_clazz_args = examine_class(clazz_args[0])
            return root.decode(root, optional_clazz, optional_clazz_args, data)

        # Try all of the remaining types one at a time.
        # We can possibly do better by examining fields.
        for clazz_arg in clazz_args:
            try:
                optional_clazz, optional_clazz_args = examine_class(clazz_arg)
                return root.decode(root, optional_clazz, optional_clazz_args, data)
            except:  # noqa: E722
                pass

        # We didn't find anything, lets just give up.
        raise ValueError

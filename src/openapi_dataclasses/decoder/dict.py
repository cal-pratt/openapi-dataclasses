from typing import Any, Iterable

from .handler import Clazz, ClazzArgs, Data, DecoderHandler, Obj


class DictHandler(DecoderHandler):
    def decode(
        self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data
    ) -> Obj:
        if len(clazz_args) == 0:
            clazz_args = [Any, Any]  # type: ignore
        elif len(clazz_args) != 2:
            raise ValueError

        key_clazz, key_args = self.examine_class(clazz_args[0])
        val_clazz, val_args = self.examine_class(clazz_args[1])

        if isinstance(data, dict):
            stream = ((key, val) for key, val in data.items())
        elif isinstance(data, Iterable):
            stream = ((key, val) for key, val in data)
        else:
            raise ValueError

        return {
            root.decode(root, key_clazz, key_args, key): root.decode(
                root, val_clazz, val_args, val
            )
            for key, val in stream
        }

from typing import Any

from .handler import Clazz, ClazzArgs, Data, DecoderHandler, Obj


class UnionHandler(DecoderHandler):
    def decode(
        self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data
    ) -> Obj:
        if len(clazz_args) == 0:
            clazz_args = [Any]  # type: ignore
        for clazz_arg in clazz_args:
            try:
                optional_clazz, optional_clazz_args = self.examine_class(clazz_arg)
                return root.decode(root, optional_clazz, optional_clazz_args, data)
            except:  # noqa: E722
                pass
        raise ValueError

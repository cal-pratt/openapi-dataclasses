from typing import Any

from .handler import Clazz, ClazzArgs, Data, DecoderHandler, Obj


class IterHandler(DecoderHandler):
    def decode(
        self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data
    ) -> Obj:
        """
        This is a helper method for all of the iterable types. We can create a generator
        and provide that to the constructor of the different list types.
        """

        if len(clazz_args) == 0:
            clazz_args = [Any]  # type: ignore
        elif len(clazz_args) != 1:
            raise ValueError

        element_clazz, element_args = self.examine_class(clazz_args[0])
        return clazz(
            root.decode(root, element_clazz, element_args, element) for element in data
        )


class SequenceHandler(IterHandler):
    def decode(
        self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data
    ) -> Obj:
        return super().decode(root, list, clazz_args, data)

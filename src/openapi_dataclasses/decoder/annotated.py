from typing import Any

from .handler import DecoderHandler, Clazz, ClazzArgs, Data, Obj


class AnnotatedHandler(DecoderHandler):
    def decode(self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data) -> Obj:
        """
        The simplest form. We can assume that we can just return whatever data is provided.
        """

        if len(clazz_args) == 0:
            clazz_args = [Any]

        annotated_clazz, annotated_clazz_args = self.examine_class(clazz_args[0])
        return root.decode(root, annotated_clazz, annotated_clazz_args, data)

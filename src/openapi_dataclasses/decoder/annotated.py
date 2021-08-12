from typing import Any

from .handler import Clazz, ClazzArgs, Data, DecoderHandler, Obj
from .util import examine_class


class AnnotatedHandler(DecoderHandler):
    def decode(
        self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data
    ) -> Obj:
        """
        The simplest form. We can assume that we can just return whatever data is provided.
        """

        if len(clazz_args) == 0:
            clazz_args = [Any]  # type: ignore

        annotated_clazz, annotated_clazz_args = examine_class(clazz_args[0])
        return root.decode(root, annotated_clazz, annotated_clazz_args, data)

from .handler import DecoderHandler, Clazz, ClazzArgs, Data, Obj


class AnyHandler(DecoderHandler):
    def decode(self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data) -> Obj:
        """
        The simplest form. We can assume that we can just return whatever data is provided.
        """

        return data
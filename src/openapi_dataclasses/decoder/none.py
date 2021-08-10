from .handler import Clazz, ClazzArgs, Data, DecoderHandler, Obj


class NoneHandler(DecoderHandler):
    def decode(
        self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data
    ) -> Obj:
        if len(clazz_args) != 0:
            raise ValueError
        if data is not None:
            raise ValueError
        return None

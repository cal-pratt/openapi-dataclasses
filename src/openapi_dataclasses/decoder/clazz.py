from .handler import Clazz, ClazzArgs, Data, DecoderHandler, Obj


class ClassHandler(DecoderHandler):
    def decode(
        self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data
    ) -> Obj:
        """
        This method will get hit by most of the primitive values. The class is used to instantiate
        the value to the correct type to avoid type inconsistency (say between int and float).
        """

        return clazz(data)

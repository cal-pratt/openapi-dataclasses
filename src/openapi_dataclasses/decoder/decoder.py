from typing import Optional

from .handler import Clazz, Data, DecoderHandler, Obj
from .root import RootHandler


class Decoder:
    def __init__(self, root_handler: Optional[DecoderHandler] = None) -> None:
        """
        This class attempts to decode a basic JSON like structure into a class objects based on a
        given input type. A number of types have already been defined for the users such as lists,
        dicts, set, dataclasses, unions, and more. Depending on the complexity of the class, a
        special handler can be provided for whatever other classes you may need.
        """

        if root_handler is None:
            root_handler = RootHandler()

        self.root_handler = root_handler

    def decode(self, clazz: Clazz, data: Data) -> Obj:
        decode_clazz, decode_clazz_args = self.root_handler.examine_class(clazz)
        return self.root_handler.decode(
            self.root_handler, decode_clazz, decode_clazz_args, data
        )

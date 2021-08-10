import dataclasses
from collections import Sequence
from typing import Annotated, Any, Optional, Union

from .annotated import AnnotatedHandler
from .any import AnyHandler
from .clazz import ClassHandler
from .dataclass import DataclassHandler
from .dict import DictHandler
from .handler import Clazz, ClazzArgs, Data, DecoderHandler, Obj
from .iter import IterHandler, SequenceHandler
from .none import NoneHandler
from .union import UnionHandler


class RootHandler(DecoderHandler):
    def __init__(self) -> None:
        """
        This class attempts to decode a basic JSON like structure into a class objects based on a
        given input type. A number of types have already been defined for the users such as lists,
        dicts, set, dataclasses, unions, and more. Depending on the complexity of the class, a
        special handler can be provided for whatever other classes you may need.
        """

        self._default_class_handler = ClassHandler()
        self._default_dataclass_handler = DataclassHandler()

        self._handlers: dict[Any, DecoderHandler] = {
            # The None class is special. Need to cast it with type
            type(None): NoneHandler(),
            Any: AnyHandler(),
            Annotated: AnnotatedHandler(),
            Union: UnionHandler(),
            # Optional[T] types get resolved as Union[T, None]. Kept here for transparency.
            Optional: UnionHandler(),
            dict: DictHandler(),
            tuple: IterHandler(),
            list: IterHandler(),
            set: IterHandler(),
            frozenset: IterHandler(),
            # Assume a sequence to be a list. Might be nice to make configurable...
            Sequence: SequenceHandler(),
        }

    def register_handler(self, clazz: Clazz, handler: DecoderHandler) -> None:
        self._handlers[clazz] = handler

    def decode(
        self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data
    ) -> Obj:
        if clazz not in self._handlers:
            if dataclasses.is_dataclass(clazz):
                # This is where the fun lives.
                self._handlers[clazz] = self._default_dataclass_handler
            else:
                # Assume its the most generic case, then keep moving on.
                self._handlers[clazz] = self._default_class_handler

        return self._handlers[clazz].decode(self, clazz, clazz_args, data)

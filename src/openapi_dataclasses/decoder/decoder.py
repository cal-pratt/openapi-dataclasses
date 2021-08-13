import dataclasses
from collections.abc import Sequence
from typing import (
    Annotated,
    Any,
    Generator,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)

from .annotated import AnnotatedHandler
from .any import AnyHandler
from .clazz import ClassHandler
from .dataclass import DataclassHandler
from .dict import DictHandler
from .handler import DecoderHandler
from .iter import IterHandler
from .none import NoneHandler
from .union import UnionHandler
from .util import get_cached_class_args

T = TypeVar("T")


class Decoder:
    def __init__(self) -> None:
        """
        This class attempts to decode a basic JSON like structure into a class objects based on a
        given input type. A number of types have already been defined for the users such as lists,
        dicts, set, dataclasses, unions, and more. Depending on the complexity of the class, a
        special handler can be provided for whatever other classes you may need.
        """

        self._class_handler = ClassHandler()
        self._dataclass_handler = DataclassHandler()
        self._iter_handler = IterHandler()

        # These are the basic decoders that will handle 99% of usecases.
        self._handlers: dict[Any, DecoderHandler] = {
            # The None class is special. Need to cast it with type
            type(None): NoneHandler(),
            Any: AnyHandler(),
            Annotated: AnnotatedHandler(),
            Union: UnionHandler(),
            # Optional[T] types get resolved as Union[T, None]. Kept here for transparency.
            Optional: UnionHandler(),
            dict: DictHandler(),
            tuple: self._iter_handler,
            list: self._iter_handler,
            set: self._iter_handler,
            frozenset: self._iter_handler,
            Sequence: self._iter_handler,
        }

    def register_handler(self, clazz: Any, handler: DecoderHandler) -> None:
        self._handlers[clazz] = handler

    def decode(self, clazz: Type[T], data: Any) -> T:
        """
        This is the basic decoder method. Decoders are able to communicate with one another by
        yielding any classes they cannot decode via yield calls. This method is responsible for
        finding the best decoder to use whenever any yield is made.
        """

        clazz_origin, _ = get_cached_class_args(clazz)

        if clazz_origin not in self._handlers:
            if dataclasses.is_dataclass(clazz_origin):
                # This is where the fun lives.
                self._handlers[clazz_origin] = self._dataclass_handler
            else:
                # Assume its the most generic case, then keep moving on.
                self._handlers[clazz_origin] = self._class_handler

        decoder_gen = self._handlers[clazz_origin].decode(clazz, data)

        # The simplest case is when there is no yield and the value is simply returned.
        if not isinstance(decoder_gen, Generator):
            return cast(T, decoder_gen)

        # Otherwise we need to help the generator decode sub components.
        try:
            # The first time we call this we don't need to send anything.
            next_clazz, next_data = next(decoder_gen)
            while True:
                decoded_data = self.decode(next_clazz, next_data)
                next_clazz, next_data = decoder_gen.send(decoded_data)
        # happens when return is made during next or send methods.
        except StopIteration as e:
            return cast(T, e.value)

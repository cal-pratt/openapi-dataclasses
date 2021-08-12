from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Sequence
from typing import Any, Callable, Type

Clazz = Type[Any]
ClazzArgs = Sequence[Type[Any]]
Data = Any
Obj = Any
Handler = Callable[[Clazz, ClazzArgs, Data], Obj]


class DecoderHandler(ABC):
    @abstractmethod
    def decode(
        self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data
    ) -> Obj:
        """
        The basic decoder method takes a class, its generic arguments, the current data representing
        that class, and converts the data into an instance of the class.

        The root handler can be called to handle any data-types you aren't able to handle yourself.
        """

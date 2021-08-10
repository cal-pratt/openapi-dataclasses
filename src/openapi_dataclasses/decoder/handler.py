from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Sequence
from typing import Any, Callable, Type, get_args, get_origin

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

    @staticmethod
    def examine_class(field_type: Clazz) -> tuple[Clazz, ClazzArgs]:
        """
        Helper method to inspect class types.
        For a given class, determine the class to instantiate, and any generic arguments.
        """

        # If the type is generic, this will be the class to use to instantiate
        field_type_origin = get_origin(field_type)

        # Try to use the mapping type, otherwise fall back to the annotation
        field_clazz = field_type_origin or field_type

        # If the type is generic, this will be the generic parameters
        field_type_args = get_args(field_type)

        return field_clazz, field_type_args

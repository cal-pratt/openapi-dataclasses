from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Any, Type

HandlerResponse = Generator[tuple[Type[Any], Any], Any, Any]


class DecoderHandler(ABC):
    @abstractmethod
    def decode(self, clazz: Type[Any], data: Any) -> HandlerResponse:
        """
        The basic decoder generator takes a class, and the data representing that class.

        It will convert the data into the class type and return it.

        Any data which cannot be converted directly by can be yielded by the generator, by yielding
        the type and the data representing that type. The yield will be followed by a send that
        will provide the converted version of that class.

        A yield should always handle the return value of that yield call.

        This structure easily allows providing decoders of complex structures.

        Example, say the fizzbuzz structure uses an array for it's values. One could do:

        .. code-block:: python

            class FizzBuzzDecoder(ABC):
                def decode(self, clazz: Clazz, data: Data) -> DecoderResponse:
                    return FizzBuzz(
                        fizz=(yield Fizz, data[0:3]),
                        buzz=(yield Buzz, data[3:6]),
                    )
            ...
            decoder.register(FizzBuzz, FizzBuzzDecoder())
            decoder.register(Fizz, FizzDecoder())
            decoder.register(Buzz, BuzzDecoder())

        This can also help in the case where strings are used instead of real types.

        .. code-block:: python

            class StringAnnotationDecoder(ABC):
                def decode(self, clazz: Clazz, data: Data) -> DecoderResponse:
                    if clazz == "SomeStringClass":
                        return (yield mymodule.SomeStringClass, data)
            ...
            decoder.register("SomeStringClass", StringAnnotationDecoder())
        """

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Any, Generic, Optional, Sequence, TypeVar

import pytest

from openapi_dataclasses.decoder import Decoder


@pytest.fixture()
def decoder():
    return Decoder()


@dataclass
class AnyClass:
    foo: Any


@dataclass(frozen=True)
class IntClass:
    foo: int


@dataclass
class FloatClass:
    foo: float


@dataclass
class StrClass:
    foo: str


@dataclass
class DictClass:
    foo: dict[str, IntClass]


@dataclass
class ListClass:
    foo: list[IntClass]


@dataclass
class AnnotatedClass:
    foo: Annotated[IntClass, "some annotation"]


@dataclass
class OptionalClass:
    foo: Optional[IntClass]


@dataclass
class SequenceClass:
    foo: Sequence[int]


@dataclass
class RecursiveClass:
    foo: list[RecursiveClass]


@pytest.mark.parametrize(
    "test_class,raw_data,expected",
    [
        (
            AnyClass,
            {"foo": {"1.234"}},
            AnyClass({"1.234"}),
        ),
        (
            IntClass,
            {"foo": "1"},
            IntClass(1),
        ),
        (
            FloatClass,
            {"foo": "1.234"},
            FloatClass(1.234),
        ),
        (
            StrClass,
            {"foo": {"1.234"}},
            StrClass("{'1.234'}"),
        ),
        (
            list[AnyClass],
            [{"foo": {"1.234"}}],
            [AnyClass({"1.234"})],
        ),
        (
            set[IntClass],
            [{"foo": "1"}],
            {IntClass(1)},
        ),
        (
            frozenset[IntClass],
            [{"foo": "1"}],
            frozenset({IntClass(1)}),
        ),
        (
            tuple[FloatClass],
            [{"foo": "1.234"}],
            (FloatClass(1.234),),
        ),
        (
            dict[str, StrClass],
            {"foo": {"foo": {"1.234"}}},
            {"foo": StrClass("{'1.234'}")},
        ),
        (
            # Can allow complex dict types by doing tuple arrays
            dict[IntClass, StrClass],
            [({"foo": "1"}, {"foo": {"1.234"}})],
            {IntClass(1): StrClass("{'1.234'}")},
        ),
        (
            DictClass,
            {"foo": {"bar": {"foo": 1}}},
            DictClass({"bar": IntClass(1)}),
        ),
        (
            ListClass,
            {"foo": [{"foo": 1}]},
            ListClass([IntClass(1)]),
        ),
        (
            AnnotatedClass,
            {"foo": {"foo": 1}},
            AnnotatedClass(IntClass(1)),
        ),
        (
            OptionalClass,
            {"foo": None},
            OptionalClass(None),
        ),
        (
            OptionalClass,
            {"foo": {"foo": 1}},
            OptionalClass(IntClass(1)),
        ),
        (
            SequenceClass,
            {"foo": (1, 2, 3)},
            SequenceClass([1, 2, 3]),
        ),
        (
            RecursiveClass,
            {"foo": [{"foo": []}]},
            RecursiveClass([RecursiveClass([])]),
        ),
    ],
)
def test_simple_types(test_class, raw_data, expected, decoder):
    actual = decoder.decode(test_class, raw_data)
    assert actual == expected


T = TypeVar("T")
U = TypeVar("U")


@dataclass
class GenericClassA(Generic[T, U]):
    foo: U
    bar: T


def test_generic_types(decoder):
    raw_data = {"foo": "1", "bar": "2"}
    expected = GenericClassA("1", 2)
    actual = decoder.decode(GenericClassA[int, str], raw_data)
    assert actual == expected


@dataclass
class NestedGenericClassA(Generic[T]):
    foo: T


@dataclass
class NestedGenericClassB(Generic[T, U]):
    foo: list[NestedGenericClassA[U]]
    bar: T


def test_nested_generic_types(decoder):
    raw_data = {"foo": [{"foo": "1"}], "bar": "2"}
    expected = NestedGenericClassB([NestedGenericClassA("1")], 2)
    actual = decoder.decode(NestedGenericClassB[int, str], raw_data)
    assert actual == expected

import dataclasses
from collections.abc import Sequence
from functools import cache
from typing import Any, Type, get_args, get_origin, get_type_hints


@cache
def get_cached_type_hints(clazz: Type[Any]) -> dict[str, Type[Any]]:
    """
    This cached method reduces the time of decoding some specs by up to 90%
    """
    return get_type_hints(clazz)


@cache
def get_cached_fields(clazz: Type[Any]) -> tuple[dataclasses.Field, ...]:
    return dataclasses.fields(clazz)  # type: ignore


@cache
def get_cached_class_args(clazz: Type[Any]) -> tuple[Type[Any], Sequence[Type[Any]]]:
    """
    Helper function to inspect class types.
    For a given class, determine the class to instantiate, and any generic arguments.

    e.g.
    Dict[str, int] -> (dict, (str, int))
    Foo -> (Foo, (,))
    """

    # If the type is generic, this will be the class to use to instantiate
    # This will be None if the class is not generic.
    clazz_origin = get_origin(clazz) or clazz

    # If the type is generic, this will be the generic parameters
    # This will be an empty tuple if the class is not generic.
    clazz_args = get_args(clazz)

    return clazz_origin, clazz_args

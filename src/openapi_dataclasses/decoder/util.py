import dataclasses
from functools import cache
from typing import get_args, get_origin, get_type_hints

from .handler import Clazz, ClazzArgs


@cache
def get_cached_type_hints(clazz: Clazz) -> dict[str, Clazz]:
    """
    This cached method reduces the time of decoding some specs by up to 90%
    """
    return get_type_hints(clazz)


@cache
def get_cached_fields(clazz: Clazz) -> tuple[dataclasses.Field, ...]:
    return dataclasses.fields(clazz)  # type: ignore


@cache
def examine_class(field_type: Clazz) -> tuple[Clazz, ClazzArgs]:
    """
    Helper function to inspect class types.
    For a given class, determine the class to instantiate, and any generic arguments.
    """

    # If the type is generic, this will be the class to use to instantiate
    field_type_origin = get_origin(field_type)

    # Try to use the mapping type, otherwise fall back to the annotation
    field_clazz = field_type_origin or field_type

    # If the type is generic, this will be the generic parameters
    field_type_args = get_args(field_type)

    return field_clazz, field_type_args

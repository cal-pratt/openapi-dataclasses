from typing import Any, Type

from .handler import DecoderHandler, HandlerResponse
from .util import (
    get_cached_class_args,
    get_cached_fields,
    get_cached_type_hints,
)


class DataclassHandler(DecoderHandler):
    def decode(self, clazz: Type[Any], data: Any) -> HandlerResponse:
        clazz_origin, clazz_args = get_cached_class_args(clazz)
        resolved_hints = get_cached_type_hints(clazz_origin)
        kwargs = {}

        # Handling generic dataclasses makes this story a lot harder, but not impossible.
        # First thing we need to do is determine if there are generic types provided, and
        # if there are we need to resolve them.
        #
        # In order to resolve the types, we can assume that the classes typevar parameters
        # match up one to one with the class args provided. Then for each of the resolved
        # type hints in the class, we need to replace the typevar version with the real class
        # from the class args input.
        #
        # To get trickier, the typevars themselves might be nested. e.g. List[Optional[T]].
        # To handle this case we need to recursively break apart the types to find any typevar
        # parameters, and then reconstruct them with the substituted values.
        #
        # See https://stackoverflow.com/q/68731193/3280538
        if clazz_args and hasattr(clazz_origin, "__parameters__"):
            typevars = dict(zip(clazz_origin.__parameters__, clazz_args))

            def reconstruct_args(hint):
                hint_clazz, hint_args = get_cached_class_args(hint)

                # If the typevar is already popped out, no need to keep looking.
                if hint_clazz in typevars:
                    return typevars[hint_clazz]

                # The class can't be reconstructed. No way to try? Might never need to?
                if not hasattr(hint_clazz, "__class_getitem__"):
                    return hint

                # Recursively clean up the child arguments.
                hint_args = tuple(
                    (typevars.get(hint_arg) or reconstruct_args(hint_arg))
                    for hint_arg in hint_args
                )

                # Reconstruct the container type.
                return hint_clazz.__class_getitem__(hint_args)

            for field_name in resolved_hints:
                resolved_hints[field_name] = reconstruct_args(
                    resolved_hints[field_name]
                )

        for clazz_field in get_cached_fields(clazz_origin):
            python_name = field_name = clazz_field.name
            metadata = clazz_field.metadata.get("openapi_dataclasses", {})
            if "name" in metadata:
                field_name = metadata["name"]

            if field_name in data:
                if "decoder" in metadata:
                    kwargs[python_name] = metadata["decoder"](data[field_name])
                else:
                    kwargs[python_name] = (
                        yield resolved_hints[python_name],
                        data[field_name],
                    )

        return clazz_origin(**kwargs)

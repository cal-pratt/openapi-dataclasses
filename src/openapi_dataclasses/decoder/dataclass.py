from .handler import Clazz, ClazzArgs, Data, DecoderHandler, Obj
from .util import examine_class, get_cached_fields, get_cached_type_hints


class DataclassHandler(DecoderHandler):
    def decode(
        self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data
    ) -> Obj:
        resolved_hints = get_cached_type_hints(clazz)
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
        if clazz_args and hasattr(clazz, "__parameters__"):
            typevars = dict(zip(clazz.__parameters__, clazz_args))

            def reconstruct_args(hint):
                hint_clazz, hint_args = examine_class(hint)

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

        for clazz_field in get_cached_fields(clazz):
            python_name = field_name = clazz_field.name
            metadata = clazz_field.metadata.get("openapi_dataclasses", {})
            if "name" in metadata:
                field_name = metadata["name"]

            if field_name in data:
                if "decoder" in metadata:
                    kwargs[python_name] = metadata["decoder"](data[field_name])
                else:
                    field_clazz, field_args = examine_class(resolved_hints[python_name])
                    kwargs[python_name] = root.decode(
                        root, field_clazz, field_args, data[field_name]
                    )

        return clazz(**kwargs)

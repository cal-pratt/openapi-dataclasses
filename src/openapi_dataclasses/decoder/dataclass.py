import dataclasses
from typing import get_type_hints

from .handler import DecoderHandler, Clazz, ClazzArgs, Data, Obj


class DataclassHandler(DecoderHandler):
    def decode(self, root: DecoderHandler, clazz: Clazz, clazz_args: ClazzArgs, data: Data) -> Obj:
        resolved_hints = get_type_hints(clazz)
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
                hint_clazz, hint_args = self.examine_class(hint)

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
                resolved_hints[field_name] = reconstruct_args(resolved_hints[field_name])

        for clazz_field in dataclasses.fields(clazz):
            field_name = clazz_field.name
            if field_name in data:
                field_clazz, field_args = self.examine_class(resolved_hints[field_name])
                kwargs[field_name] = root.decode(root, field_clazz, field_args, data[field_name])

        return clazz(**kwargs)

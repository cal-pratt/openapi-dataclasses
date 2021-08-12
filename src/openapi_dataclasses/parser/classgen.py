from collections import defaultdict
from typing import Iterator

from ..types.openapi import OpenApiSchema, OpenApiSpec
from ..types.python import (
    PythonClassAttribute,
    PythonEnumAttribute,
    PythonImport,
)
from .constants import MODELS_PACKAGE
from .formatter import enum2attribute, property2attribute
from .reference import PythonContext

BASIC_TYPES: dict[str, str] = {
    "integer": "int",
    "string": "str",
    "number": "float",
    "boolean": "bool",
}


def find_references(schema: OpenApiSchema) -> Iterator[str]:
    """
    Determine any references in this class and return to the caller.
    This method needs to be recursive to account for nest type composition.
    """

    if schema.ref:
        yield schema.ref

    if schema.items:
        yield "List"

    # If items is non-empty is set we're in an array type
    if schema.items:
        if isinstance(schema.items, list):
            for item in schema.items:
                yield from find_references(item)
        else:
            yield from find_references(schema.items)

    if isinstance(schema.additional_items, OpenApiSchema):
        yield from find_references(schema.additional_items)

    # If properties is non-empty is set we're in an object type
    for prop in schema.properties.values():
        yield from find_references(prop)

    if schema.additional_properties:
        yield "Dict"

    # When additional_properties is True we will assume the type is dict[str, Any]
    if schema.additional_properties is True:
        yield "Any"

    # When additional_properties is an object we have to recurse into its contents
    if isinstance(schema.additional_properties, OpenApiSchema):
        yield from find_references(schema.additional_properties)

    # When nullable is True we will assume the type is Optional[T]
    if schema.nullable:
        # TODO [KnownLimitation]: NULLABLE_TYPES
        # Need to add Optional to the imports if nullable is True
        pass


def update_model_imports(
    openapi_spec: OpenApiSpec, class_contexts: dict[str, PythonContext]
) -> None:
    """
    For each of the models, determine if they reference other models.
    If they do, then we need to import them when generating the model class.
    We will update each context with any references we discover.
    """

    for current_ref, current_context in class_contexts.items():
        # Extra assurance we're not doing anything funky
        if current_context.package_name != MODELS_PACKAGE:
            continue

        schema = openapi_spec.components.schemas[current_context.openapi_name]
        module_imports: dict[str, set[str]] = defaultdict(set)
        for discovered_reference in find_references(schema):
            # Ignore recursive references
            if discovered_reference == current_context.ref:
                continue
            # Handle typing module imports separately
            elif discovered_reference in ("Any", "List", "Dict", "Optional"):
                module_imports["typing"].add(discovered_reference)
            # Use the contexts dict to determine the paths of other the models
            else:
                import_class_context = class_contexts[discovered_reference]
                import_module_name = f".{import_class_context.module_name}"
                import_class_name = import_class_context.class_name
                module_imports[import_module_name].add(import_class_name)

        current_context.module_imports = [
            PythonImport(import_module, sorted(list(names)))
            for import_module, names in module_imports.items()
        ]


def find_attribute_type(
    *,
    class_contexts: dict[str, PythonContext],
    current_class_name: str,
    schema: OpenApiSchema,
) -> str:
    # TODO [KnownLimitation]: NULLABLE_TYPES
    # Need to wrap the type in Optional if nullable is True

    if schema.ref:
        discovered_class_name = class_contexts[schema.ref].class_name
        if discovered_class_name == current_class_name:
            # Handle the case of forward references gracefully
            return f'"{discovered_class_name}"'
        else:
            return discovered_class_name

    # TODO [KnownLimitation]: MULTIPLE_SCHEMA_TYPES
    # Need to handle Union type if there are multiple types involved.
    # find_references should check to see if a union is needed
    elif basic_type := next(filter(None, map(BASIC_TYPES.get, schema.type)), None):
        return basic_type

    elif schema.items:
        if (
            schema.type is not None
            and len(schema.type) > 0
            and "array" not in schema.type
        ):
            raise ValueError(f"Invalid schema reference {current_class_name}: {schema}")

        # TODO [KnownLimitation]: MULTIPLE_ITEM_TYPES
        # Need to handle Union type in this event.
        # find_references should check to see if a union is needed
        if isinstance(schema.items, list):
            item = schema.items[0]
        else:
            item = schema.items

        discovered_type = find_attribute_type(
            class_contexts=class_contexts,
            current_class_name=current_class_name,
            schema=item,
        )
        return f"List[{discovered_type}]"

    # TODO [KnownLimitation]: PROPS_AND_ADDITIONAL_PROPS
    # Need to handle the case where there are both known and unknown prop types
    # TODO [KnownLimitation]: INNER_PROPS
    # Need to handle the case where a property has properties
    elif schema.properties:
        raise ValueError("Cannot handle nested properties")

    elif schema.additional_properties is True:
        return "Dict[str, Any]"

    elif isinstance(schema.additional_properties, OpenApiSchema):
        discovered_type = find_attribute_type(
            class_contexts=class_contexts,
            current_class_name=current_class_name,
            schema=schema.additional_properties,
        )
        return f"Dict[str, {discovered_type}]"

    else:
        raise ValueError


def update_model_attributes(
    openapi_spec: OpenApiSpec, class_contexts: dict[str, PythonContext]
) -> None:

    for current_context in class_contexts.values():
        # Extra assurance we're not doing anything funky
        if current_context.package_name != MODELS_PACKAGE:
            continue

        schema = openapi_spec.components.schemas[current_context.openapi_name]
        if schema.enum and schema.properties:
            raise ValueError(
                f"Component Schema is not a valid enum or object type: {schema}"
            )

        # TODO [KnownLimitation]: TOP_LEVEL_ADDITIONAL_PROPS
        # Need to handle the case where the component schema has additional props
        if schema.additional_properties:
            raise ValueError(
                f"Component Schema is not a valid enum or object type: {schema}"
            )

        # TODO [KnownLimitation]: TOP_LEVEL_ARRAY
        # Need to handle the case where the component schema has additional props
        if schema.items or schema.additional_items:
            raise ValueError(
                f"Component Schema is not a valid enum or object type: {schema}"
            )

        if schema.enum:
            # TODO [KnownLimitation]: NON_STRING_ENUM
            # Handle the case where enums are not strings.
            if schema.type != ["string"]:
                raise ValueError(f"Only string enum values are supported: {schema}")

            enum_attributes: list[PythonEnumAttribute] = []
            for enum in schema.enum:
                attribute_name = enum2attribute(enum)
                attribute_value = f'"{enum}"'
                enum_attributes.append(
                    PythonEnumAttribute(
                        attribute_name=attribute_name,
                        attribute_value=attribute_value,
                    )
                )

            current_context.enum_attributes = enum_attributes
        else:
            class_attributes: list[PythonClassAttribute] = []
            for property_name, property_schema in schema.properties.items():
                attribute_name = property2attribute(property_name)
                attribute_type = find_attribute_type(
                    class_contexts=class_contexts,
                    current_class_name=current_context.class_name,
                    schema=property_schema,
                )
                class_attributes.append(
                    PythonClassAttribute(
                        attribute_name=attribute_name,
                        openapi_name=property_name,
                        attribute_type=attribute_type,
                        attribute_default="None",
                    )
                )

            current_context.class_attributes = class_attributes

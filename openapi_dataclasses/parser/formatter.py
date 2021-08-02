from keyword import iskeyword

import inflection


def schema2class(schema_name: str) -> str:
    to_camel = inflection.camelize(schema_name.replace("-", "_")).replace("_", "")
    to_snake = inflection.underscore(to_camel)
    return inflection.camelize(to_snake)


def property2attribute(property_name: str) -> str:
    property_name = inflection.underscore(property_name).replace("-", "_").lower()
    if iskeyword(property_name) or property_name in ("unhandled_data", "openapi_field"):
        return f"{property_name}_val"
    return property_name


def enum2attribute(enum_name: str) -> str:
    return inflection.underscore(enum_name).upper().replace("-", "_")


def class2module(class_name: str) -> str:
    return inflection.underscore(class_name)

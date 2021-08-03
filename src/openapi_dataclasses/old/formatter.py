# import json
# from keyword import iskeyword
# from typing import Any
#
# import inflection
#
#
# class Formatter:
#     @staticmethod
#     def schema2class(schema_name: str) -> str:
#         to_camel = inflection.camelize(schema_name.replace("-", "_")).replace("_", "")
#         to_snake = inflection.underscore(to_camel)
#         return inflection.camelize(to_snake)
#
#     @staticmethod
#     def property2attribute(property_name: str) -> str:
#         property_name = inflection.underscore(property_name).replace("-", "_").lower()
#         if iskeyword(property_name):
#             return f"{property_name}_val"
#         return property_name
#
#     @staticmethod
#     def enum2attribute(enum_name: str) -> str:
#         return inflection.underscore(enum_name).upper().replace("-", "_")
#
#     @staticmethod
#     def class2module(class_name: str) -> str:
#         return inflection.underscore(class_name)
#
#     @staticmethod
#     def schema2json(schema: dict[str, Any]) -> str:
#         schema = dict(**schema)
#         key = schema["ref"].split("/")[-1]
#         del schema["ref"]
#         del schema["class"]
#         return f'"{key}": ' + json.dumps(schema, indent=2)
#
#     @staticmethod
#     def operation2json(operation: dict[str, Any]) -> str:
#         operation = dict(**operation)
#         path = operation["path"]
#         method = operation["method"]
#         del operation["path"]
#         del operation["method"]
#         del operation["class"]
#         return f'"{path}": ' + json.dumps({method: operation}, indent=2)

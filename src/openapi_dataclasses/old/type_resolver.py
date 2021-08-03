# from collections import defaultdict
# from typing import Any
#
# from .schemareference import SchemaReference
#
# basic_types = {
#     "integer": "int",
#     "string": "str",
#     "number": "float",
#     "boolean": "bool",
# }
#
#
# class TypeResolver:
#     def __init__(
#         self,
#         *,
#         schema_reference: SchemaReference,
#         module_name: str,
#         class_name: str,
#         relative_import: str = ".",
#     ) -> None:
#         self.schema_reference = schema_reference
#         self.module_name = module_name
#         self.class_name = class_name
#         self.relative_import = relative_import
#
#         self.required_imports: dict[str, set[str]] = defaultdict(set)
#
#     def resolve_ref_type(self, property_ref: str) -> str:
#         property_class_name = self.schema_reference.find_class_for_ref(property_ref)
#         property_module_name = self.schema_reference.find_module_for_ref(property_ref)
#
#         if property_module_name != self.module_name:
#             relative_module_name = f"{self.relative_import}{property_module_name}"
#             self.required_imports[relative_module_name].add(property_class_name)
#             return property_class_name
#         else:
#             return f'"{property_class_name}"'
#
#     def resolve_object_type(self, property_data: dict[str, Any]) -> str:
#         if x_props := property_data.get("additionalProperties"):
#             if x_props is True:
#                 self.required_imports["typing"].add("Any")
#                 return "dict[str, Any]"
#             elif "$ref" in x_props:
#                 return f'dict[str, {self.resolve_ref_type(x_props.get("$ref"))}]'
#             elif x_props["type"] in basic_types:
#                 return f'dict[str, {basic_types[x_props["type"]]}]'
#             elif x_props["type"] == "object":
#                 return f'dict[str, {self.resolve_object_type(x_props)}]'
#             else:
#                 raise ValueError(f"Found unsupported prop: {self.class_name=}")
#         else:
#             raise ValueError(f"Found unsupported prop: {self.class_name=}")
#
#     def _resolve_property_type(self, property_data: dict[str, Any],
#     is_list: bool) -> tuple[str, bool]:
#         if property_type := property_data.get("type"):
#             if property_type in basic_types:
#                 return basic_types[property_type], is_list
#             elif property_type == "array":
#                 if is_list:
#                     raise ValueError(f"Nested list parsing not supported {self.class_name=}")
#                 return self._resolve_property_type(property_data["items"], is_list=True)
#             elif property_type == "object":
#                 if property_type := self.resolve_object_type(property_data):
#                     return property_type, is_list
#             else:
#                 print(f"Found unsupported prop: {self.class_name=}")
#         elif property_ref := property_data.get("$ref"):
#             return self.resolve_ref_type(property_ref), is_list
#         else:
#             print(f"Found unsupported prop: {self.class_name=}")
#
#     def resolve_property_type(self, property_data: dict[str, Any]) -> str:
#         property_type, is_list = self._resolve_property_type(property_data, False)
#         if is_list:
#             property_type = f"list[{property_type}]"
#         return property_type

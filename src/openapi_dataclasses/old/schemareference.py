# import json
# from collections import defaultdict
#
# from .formatter import Formatter
#
#
# supported_schema_types = {'object', 'string'}
#
#
# class SchemaReference:
#     def __init__(self, openapi_json_path: str, formatter: Formatter)-> None:
#         self.openapi_json_path = openapi_json_path
#         self.formatter = formatter
#
#         with open(openapi_json_path, "r") as openapi_json_file:
#             self.openapi_json = json.load(openapi_json_file)
#
#         self.schemas = {
#             self.formatter.schema2class(schema): {
#                 "ref": f"#/components/schemas/{schema}",
#                 "class": self.formatter.schema2class(schema),
#                 **schema_data,
#             }
#             for schema, schema_data in self.openapi_json["components"]["schemas"].items()
#         }
#
#         self.ref2class_lookup = {schema["ref"]: schema["class"] for schema in self.schemas.values()}
#
#         self.operations = {
#             self.formatter.schema2class(method_data["operationId"]): {
#                 "path": path,
#                 "method": method,
#                 "class": self.formatter.schema2class(method_data["operationId"]),
#                 **method_data,
#             }
#             for path, path_data in self.openapi_json["paths"].items()
#             for method, method_data in path_data.items()
#         }
#
#         schema_types = {schema["type"] for schema in self.schemas.values()}
#         if len(schema_types - supported_schema_types) != 0:
#             raise ValueError(f"Unknown schema types: {schema_types - supported_schema_types}")
#
#         # One to one, a class and its module
#         self.class2module_lookup: dict[str, str] = {}
#
#         # One to many, modules and their classes
#         self.models_init_imports: dict[str, list[str]] = defaultdict(list)
#
#         # Pre-populate required imports
#         for class_name, schema in self.schemas.items():
#             module_name = self.formatter.class2module(class_name)
#             self.models_init_imports[module_name].append(class_name)
#             self.class2module_lookup[class_name] = module_name
#
#         # One to many, modules and their classes
#         self.api_init_imports: dict[str, list[str]] = defaultdict(list)
#
#         # Pre-populate required imports
#         for class_name, operation in self.operations.items():
#             module_name = self.formatter.class2module(class_name)
#             self.api_init_imports[module_name].append(class_name)
#             self.class2module_lookup[class_name] = module_name
#
#     def find_class_for_ref(self, ref_name: str) -> str:
#         return self.ref2class_lookup[ref_name]
#
#     def find_ref_for_class(self, class_name: str) -> str:
#         return self.schemas[class_name]["ref"]
#
#     def find_module_for_class(self, class_name: str) -> str:
#         return self.class2module_lookup[class_name]
#
#     def find_module_for_ref(self, ref_name: str) -> str:
#         return self.find_module_for_class(self.find_class_for_ref(ref_name))

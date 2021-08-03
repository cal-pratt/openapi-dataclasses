# import time
# from collections import defaultdict
#
# from .schemareference import SchemaReference
# from .type_resolver import TypeResolver
# from .formatter import Formatter
# from .types import EnumSchema, EnumAttribute, ObjectSchema, ObjectAttribute, OperationSchema, OperationAttribute
# from .validation import validate_module
# from .templatewriter import TemplateWriter
#
#
# def generate_models(
#     *,
#     template_writer: TemplateWriter,
#     schema_reference: SchemaReference,
# ) -> None:
#     total = set(schema_reference.schemas)
#     completed = set()
#
#     for class_name, schema in schema_reference.schemas.items():
#         module_name = schema_reference.find_module_for_class(class_name)
#         schema_json = schema_reference.formatter.schema2json(schema)
#         ref = schema_reference.find_ref_for_class(class_name)
#
#         if "enum" in schema:
#             if schema["type"] != "string":
#                 raise ValueError(f"Unsupported string class: {class_name=}")
#
#             template_writer.write_models_enum_file(
#                 EnumSchema(
#                     module_name=module_name,
#                     class_name=class_name,
#                     schema_json=schema_json,
#                     ref=ref,
#                     attributes=[
#                         EnumAttribute(
#                             attr=schema_reference.formatter.enum2attribute(enum),
#                             value=enum,
#                         )
#                         for enum in schema["enum"]
#                     ],
#                 )
#             )
#         else:
#             type_resolver = TypeResolver(
#                 schema_reference=schema_reference,
#                 module_name=module_name,
#                 class_name=class_name,
#             )
#             template_writer.write_models_object_file(
#                 ObjectSchema(
#                     module_name=module_name,
#                     class_name=class_name,
#                     schema_json=schema_json,
#                     ref=ref,
#                     attributes=[
#                         ObjectAttribute(
#                             prop=property_name,
#                             attr=schema_reference.formatter.property2attribute(property_name),
#                             type=type_resolver.resolve_property_type(property_data),
#                         )
#                         for property_name, property_data in schema.get("properties", {}).items()
#                     ],
#                     imports=dict(**type_resolver.required_imports)
#                 )
#             )
#         completed.add(class_name)
#
#     print(f"Generated Models: {len(completed)} / {len(total)}")
#     for uncompleted in sorted(total - completed):
#         print(f"    Unimplemented: {uncompleted}")
#
#     template_writer.write_models_init_file(schema_reference.models_init_imports)
#
#
# path_param_mapping = {
#     'string': "str",
#     'number': "float",
#     'boolean': "bool",
#     'integer': "int",
# }
#
#
# def generate_apis(
#     *,
#     template_writer: TemplateWriter,
#     schema_reference: SchemaReference,
# ) -> None:
#     total = set(schema_reference.operations)
#     completed = set()
#
#     init_imports: dict[str, list[str]] = defaultdict(list)
#
#     for class_name, operation in schema_reference.operations.items():
#         module_name = schema_reference.find_module_for_class(class_name)
#
#         method = operation["method"].lower()
#         path = operation["path"]
#         parameters = operation.get("parameters", [])
#         responses = operation.get("responses", {})
#
#         if len(responses.keys()) != 1:
#             raise ValueError(f"Can't support multiple response types {class_name=}")
#
#         for response_key, response in responses.items():
#             if "content" not in response:
#                 schema = None
#             elif "application/json" not in response["content"]:
#                 schema = None
#             elif "schema" not in response["content"]["application/json"]:
#                 schema = None
#             else:
#                 schema = response["content"]["application/json"]["schema"]
#
#             if any(
#                 parameter["in"] == "path"
#                 and (parameter["type"] not in path_param_mapping)
#                 for parameter in parameters
#             ):
#                 raise ValueError(f"Unsupported path param type {class_name=}")
#
#             type_resolver = TypeResolver(
#                 schema_reference=schema_reference,
#                 module_name=module_name,
#                 class_name=class_name,
#                 relative_import="..models."
#             )
#
#             for parameter in parameters:
#                 if not parameter.get("required"):
#                     type_resolver.required_imports["typing"].add("Optional")
#
#             attributes = {
#                 parameter["name"]: OperationAttribute(
#                     prop=parameter["name"],
#                     attr=schema_reference.formatter.property2attribute(parameter["name"]),
#                     type=type_resolver.resolve_property_type(parameter),
#                     required=parameter.get("required", False),
#                     in_path=parameter["in"] == "path"
#                 )
#                 for parameter in parameters
#             }
#
#             init_imports[module_name].append(f"{class_name}Request")
#             if response_key == "204":
#                 response_type = "None"
#             else:
#                 init_imports[module_name].append(f"{class_name}Response")
#                 response_type = type_resolver.resolve_property_type(schema)
#
#             template_writer.write_api_operation_file(
#                 OperationSchema(
#                     module_name=module_name,
#                     class_name=class_name,
#                     schema_json=schema_reference.formatter.operation2json(operation),
#                     method=method,
#                     path=path,
#                     has_path_args=any(attribute.in_path for attribute in attributes.values()),
#                     has_query_args=any(not attribute.in_path for attribute in attributes.values()),
#                     attributes=list(attributes.values()),
#                     response_type=response_type,
#                     imports=dict(**type_resolver.required_imports),
#                 )
#             )
#             completed.add(class_name)
#
#     template_writer.write_api_init_file(init_imports)
#
#     print(f"Generated APIs: {len(completed)} / {len(total)}")
#     for uncompleted in sorted(total - completed):
#         print(f"    Unimplemented: {uncompleted}")
#
#
# def main() -> None:
#     template_writer = TemplateWriter(output_dir=".", client_module="lcu")
#     schema_reference = SchemaReference("openapi/openapi.json", Formatter())
#
#     template_writer.reset_output_dir()
#
#     print("Generating models...")
#     generate_models(
#         template_writer=template_writer,
#         schema_reference=schema_reference,
#     )
#
#     print("Generating apis...")
#     generate_apis(
#         template_writer=template_writer,
#         schema_reference=schema_reference,
#     )
#
#     time.sleep(2)
#     validate_module([template_writer.client_module, "models"])
#     validate_module([template_writer.client_module, "api"])
#
#     print("Successfully generated client!")

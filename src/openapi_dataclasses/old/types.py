# from dataclasses import dataclass
#
#
# @dataclass
# class EnumAttribute:
#     attr: str
#     value: str
#
#
# @dataclass
# class EnumSchema:
#     module_name: str
#     class_name: str
#     schema_json: str
#     ref: str
#     attributes: list[EnumAttribute]
#
#
# @dataclass
# class ObjectAttribute:
#     prop: str
#     attr: str

#
#
# @dataclass
# class ObjectSchema:
#     module_name: str
#     class_name: str
#     schema_json:  str
#     ref: str
#     attributes: list[ObjectAttribute]
#     imports: dict[str, list[str]]
#
#
# @dataclass
# class OperationAttribute:
#     prop: str
#     attr: str

#     required: bool
#     in_path: bool
#
#
# @dataclass
# class OperationSchema:
#     module_name: str
#     class_name: str
#     schema_json: str
#     method: str
#     path: str
#     has_path_args: bool
#     has_query_args: bool
#     response_type: str
#     attributes: list[OperationAttribute]
#     imports: dict[str, list[str]]

from openapi_dataclasses.parser.classgen import (
    update_model_attributes,
    update_model_imports,
)
from openapi_dataclasses.parser.reference import init_model_contexts
from openapi_dataclasses.types.openapi import OpenApiSpec
from openapi_dataclasses.types.python import (
    PythonClassAttribute,
    PythonContext,
    PythonEnumAttribute,
    PythonImport,
)


def test_simple_model():
    openapi_spec_dict = {
        "openapi": "3.0.0",
        "info": {"title": "test", "version": "1.0.0"},
        "components": {
            "schemas": {
                "Some-Complex_schema_Name": {
                    "properties": {
                        "data": {
                            "additionalProperties": {
                                "additionalProperties": True,
                                "type": "object",
                            },
                            "type": "object",
                        },
                        "reference": {
                            "$ref": "#/components/schemas/SecondSCHEMAName",
                        },
                        "inventoryType": {"type": "string"},
                    },
                    "type": "object",
                },
                "SecondSCHEMAName": {
                    "enum": ["one", "TwoTwo", "THREE"],
                    "type": "string",
                },
            }
        },
        "paths": {},
    }

    openapi_spec = OpenApiSpec.from_dict(openapi_spec_dict)
    model_contexts = init_model_contexts(openapi_spec)
    update_model_imports(openapi_spec, model_contexts)
    update_model_attributes(openapi_spec, model_contexts)

    assert model_contexts == {
        "#/components/schemas/Some-Complex_schema_Name": PythonContext(
            package_name="models",
            module_name="some_complex_schema_name",
            class_name="SomeComplexSchemaName",
            openapi_name="Some-Complex_schema_Name",
            ref="#/components/schemas/Some-Complex_schema_Name",
            module_imports=[
                PythonImport(
                    from_name="typing",
                    import_names=["Any", "Dict"],
                ),
                PythonImport(
                    from_name=".second_schema_name",
                    import_names=["SecondSchemaName"],
                ),
            ],
            class_attributes=[
                PythonClassAttribute(
                    attribute_name="data",
                    openapi_name="data",
                    attribute_type="Dict[str, Dict[str, Any]]",
                    attribute_default="None",
                ),
                PythonClassAttribute(
                    attribute_name="reference",
                    openapi_name="reference",
                    attribute_type="SecondSchemaName",
                    attribute_default="None",
                ),
                PythonClassAttribute(
                    attribute_name="inventory_type",
                    openapi_name="inventoryType",
                    attribute_type="str",
                    attribute_default="None",
                ),
            ],
            enum_attributes=[],
        ),
        "#/components/schemas/SecondSCHEMAName": PythonContext(
            package_name="models",
            module_name="second_schema_name",
            class_name="SecondSchemaName",
            openapi_name="SecondSCHEMAName",
            ref="#/components/schemas/SecondSCHEMAName",
            module_imports=[],
            class_attributes=[],
            enum_attributes=[
                PythonEnumAttribute(
                    attribute_name="ONE",
                    attribute_value='"one"',
                ),
                PythonEnumAttribute(
                    attribute_name="TWO_TWO",
                    attribute_value='"TwoTwo"',
                ),
                PythonEnumAttribute(
                    attribute_name="THREE",
                    attribute_value='"THREE"',
                ),
            ],
        ),
    }

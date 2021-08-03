from ..types.openapi import OpenApiSpec
from ..types.python import PythonContext
from .constants import MODELS_PACKAGE
from .formatter import class2module, schema2class


def init_model_contexts(openapi_spec: OpenApiSpec) -> dict[str, PythonContext]:
    """For each model in the spec components, create a python class reference"""

    contexts: dict[str, PythonContext] = {}
    for openapi_name, schema in openapi_spec.components.schemas.items():
        class_name = schema2class(openapi_name)
        module_name = class2module(class_name)
        ref = "#/components/schemas/" + openapi_name

        contexts[ref] = PythonContext(
            package_name=MODELS_PACKAGE,
            module_name=module_name,
            class_name=class_name,
            openapi_name=openapi_name,
            ref=ref,
        )

    return contexts

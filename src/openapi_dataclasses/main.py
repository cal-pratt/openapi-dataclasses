import argparse
import os
from typing import Optional

from .configuration import Configuration
from .parser.classgen import update_model_attributes, update_model_imports
from .parser.reference import init_model_contexts
from .types.openapi import OpenApiSpec
from .writer import TemplateWriter

DEFAULT_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="openapi-dataclasses")
    parser.add_argument("openapi_json")
    parser.add_argument("-m", "--client-module", default="myclient")
    parser.add_argument("-o", "--output-dir", default=".")
    parser.add_argument("-t", "--templates-dir", default=DEFAULT_TEMPLATES_DIR)
    return parser


def create_config(args: argparse.Namespace) -> Configuration:
    return Configuration(
        openapi_json=args.openapi_json,
        output_dir=args.output_dir,
        client_module=args.client_module,
        templates_dir=args.templates_dir,
    )


def main() -> Optional[int]:
    parser = create_parser()
    configuration = create_config(parser.parse_args())

    openapi_spec = OpenApiSpec.load(configuration.openapi_json)

    model_contexts = init_model_contexts(openapi_spec)
    update_model_imports(openapi_spec, model_contexts)
    update_model_attributes(openapi_spec, model_contexts)

    writer = TemplateWriter(
        output_dir=configuration.output_dir,
        client_module=configuration.client_module,
        templates_dir=configuration.templates_dir,
        default_templates_dir=DEFAULT_TEMPLATES_DIR,
    )
    writer.reset_output_dir()
    for context in model_contexts.values():
        writer.write_models_file(context)

    writer.clean_generated_code()

    return 0

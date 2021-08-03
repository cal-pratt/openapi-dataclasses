import os
import shutil
from typing import Any

from jinja2 import Template

from ..types.python import PythonContext


class TemplateWriter:
    def __init__(
        self,
        *,
        output_dir: str,
        client_module: str,
        templates_dir: str,
        default_templates_dir: str,
    ) -> None:
        self.output_dir = output_dir
        self.client_module = client_module
        self.project_dir = os.path.join(self.output_dir, self.client_module)
        self.models_module = os.path.join(self.project_dir, "models")
        self.api_module = os.path.join(self.project_dir, "api")

        self.templates_dir = templates_dir
        self.default_templates_dir = default_templates_dir

        self.models_enum_template = self.open_template("models/enum.py.j2")
        self.models_object_template = self.open_template("models/object.py.j2")
        self.models_init_template = self.open_template("models/__init__.py.j2")

        self.api_init_template = self.open_template("api/__init__.py.j2")
        self.api_operation_template = self.open_template("api/operation.py.j2")

    def open_template(self, template_path: str) -> Template:
        if os.path.exists(os.path.join(self.templates_dir, template_path)):
            path = os.path.join(self.templates_dir, template_path)
        else:
            path = os.path.join(self.default_templates_dir, template_path)
        with open(path, "r") as template_file:
            return Template(template_file.read())

    def reset_output_dir(self) -> None:
        if os.path.exists(self.project_dir):
            shutil.rmtree(self.project_dir)

        def ignore_override_func(directory: str, files: list[str]) -> list[str]:
            return [
                file
                for file in files
                if file[-3:] != ".py"
                and not os.path.isdir(os.path.join(directory, file))
            ]

        def ignore_default_func(directory: str, files: list[str]) -> list[str]:
            return [
                file
                for file in ignore_override_func(directory, files)
                if os.path.exists(os.path.join(directory, file))
            ]

        shutil.copytree(
            self.templates_dir, self.project_dir, ignore=ignore_override_func
        )
        shutil.copytree(
            self.default_templates_dir,
            self.project_dir,
            ignore=ignore_default_func,
            dirs_exist_ok=True,
        )

    @staticmethod
    def write_file(*, template: Template, filename: str, data: Any) -> None:
        with open(filename, "w") as output_file:
            output_file.write(template.render(data=data))

    def write_models_file(self, data: PythonContext) -> None:
        if data.enum_attributes:
            template = self.models_enum_template
        else:
            template = self.models_object_template
        self.write_file(
            template=template,
            filename=os.path.join(self.models_module, f"{data.module_name}.py"),
            data=data,
        )

    def write_models_init_file(self, data: dict[str, list[str]]) -> None:
        self.write_file(
            template=self.models_init_template,
            filename=os.path.join(self.models_module, "__init__.py"),
            data=data,
        )

    def write_api_init_file(self, data: dict[str, list[str]]) -> None:
        self.write_file(
            template=self.api_init_template,
            filename=os.path.join(self.api_module, "__init__.py"),
            data=data,
        )

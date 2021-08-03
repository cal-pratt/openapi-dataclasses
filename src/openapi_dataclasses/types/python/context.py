from dataclasses import dataclass, field
from typing import Optional

from .attribute import PythonClassAttribute, PythonEnumAttribute
from .imports import PythonImport


@dataclass
class PythonContext:
    """A helper class to keep track of python information given a reference name"""

    package_name: str
    module_name: str
    class_name: str
    openapi_name: str
    ref: Optional[str] = None
    module_imports: list[PythonImport] = field(default_factory=list)
    class_attributes: list[PythonClassAttribute] = field(default_factory=list)
    enum_attributes: list[PythonEnumAttribute] = field(default_factory=list)

from dataclasses import dataclass


@dataclass
class PythonImport:
    from_name: str
    import_names: list[str]
    """
    The module name to import from and list of names to import.
    """

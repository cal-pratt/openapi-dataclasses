from dataclasses import dataclass


@dataclass
class Configuration:
    openapi_json: str
    output_dir: str
    client_module: str
    templates_dir: str

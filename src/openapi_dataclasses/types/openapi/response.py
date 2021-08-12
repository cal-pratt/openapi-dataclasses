from dataclasses import dataclass


@dataclass
class OpenApiResponse:
    """
    Describes a single response from an API Operation, including design-time, static links to
    operations based on the response.
    """

from dataclasses import dataclass

from dataclasses_json import dataclass_json, CatchAll, Undefined

from .field import openapi_field


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class OpenApiParameter:
    """
    Describes a single operation parameter.
    A unique parameter is defined by a combination of a name and location.

    There are four possible parameter locations specified by the in field:

        path - Used together with Path Templating, where the parameter value is actually part of
            the operation's URL. This does not include the host or base path of the API.
            For example, in /items/{itemId}, the path parameter is itemId.

        query - Parameters that are appended to the URL.
            For example, in /items?id=###, the query parameter is id.

        header - Custom headers that are expected as part of the request.
            Note that RFC7230 states header names are case insensitive.

        cookie - Used to pass a specific cookie value to the API.
    """

    unhandled_data: CatchAll = openapi_field(default_factory=dict)

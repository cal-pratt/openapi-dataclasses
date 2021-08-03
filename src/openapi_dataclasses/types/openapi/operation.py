from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config

from .extdoc import OpenApiExternalDocumentation
from .parameter import OpenApiParameter
from .requestbody import OpenApiRequestBody
from .response import OpenApiResponse
from .server import OpenApiServer


@dataclass
class OpenApiOperation(DataClassJsonMixin):
    """
    Describes a single API operation on a path.
    """

    responses: dict[str, OpenApiResponse]
    """
    The list of possible responses as they are returned from executing this operation.

    Responses have the following keys:

        default: The documentation of responses other than the ones declared for specific HTTP 
            response codes. Use this field to cover undeclared responses. A Reference Object can 
            link to a response that the OpenAPI Object's components/responses section defines.

        status-code: Any HTTP status code can be used as the property name, but only one property 
            per code, to describe the expected response for that HTTP status code. A Reference 
            Object can link to a response that is defined in the OpenAPI Object's components/
            responses section. This field MUST be enclosed in quotation marks (for example, "200") 
            for compatibility between JSON and YAML. To define a range of response codes, this field
            MAY contain the uppercase wildcard character X. For example, 2XX represents all response 
            codes between [200-299]. Only the following range definitions are allowed: 1XX, 2XX, 
            3XX, 4XX, and 5XX. If a response is defined using an explicit code, the explicit code 
            definition takes precedence over the range definition for that code.
    """

    tags: list[str] = field(default_factory=list)
    """
    A list of tags for API documentation control. Tags can be used for logical grouping of 
    operations by resources or any other qualifier.
    """

    summary: Optional[str] = None
    """
    A short summary of what the operation does.
    """

    description: Optional[str] = None
    """
    A verbose explanation of the operation behavior.
    CommonMark syntax MAY be used for rich text representation.
    """

    external_docs: Optional[OpenApiExternalDocumentation] = field(
        metadata=config(field_name="externalDocs"), default=None
    )
    """
    Additional external documentation for this tag.
    """

    operation_id: Optional[str] = field(
        metadata=config(field_name="operationId"), default=None
    )
    """
    Unique string used to identify the operation. The id MUST be unique among all operations 
    described in the API. The operationId value is case-sensitive. Tools and libraries MAY use the 
    operationId to uniquely identify an operation, therefore, it is RECOMMENDED to follow common 
    programming naming conventions.
    """

    parameters: dict[str, OpenApiParameter] = field(default_factory=dict)
    """
    A list of parameters that are applicable for this operation. If a parameter is already defined 
    at the Path Item, the new definition will override it but can never remove it. The list MUST NOT
    include duplicated parameters. A unique parameter is defined by a combination of a name and 
    location. The list can use the Reference Object to link to parameters that are defined at the 
    OpenAPI Object's components/parameters.
    """

    request_body: Optional[OpenApiRequestBody] = field(
        metadata=config(field_name="requestBody"), default=None
    )
    """
    The request body applicable for this operation. The requestBody is only supported in HTTP 
    methods where the HTTP 1.1 specification RFC7231 has explicitly defined semantics for request 
    bodies. In other cases where the HTTP spec is vague, requestBody SHALL be ignored by consumers.
    """

    deprecated: bool = False
    """
    Declares this operation to be deprecated. Consumers SHOULD refrain from usage of the declared 
    operation. Default value is false.
    """

    security: list[dict[str, list[str]]] = field(default_factory=list)
    """
    A declaration of which security mechanisms can be used across the API. The list of values 
    includes alternative security requirement objects that can be used. Only one of the security 
    requirement objects need to be satisfied to authorize a request. Individual operations can 
    override this definition. To make security optional, an empty security requirement ({}) can be 
    included in the array.

    Each name MUST correspond to a security scheme which is declared in the Security Schemes under 
    the Components Object. If the security scheme is of type "oauth2" or "openIdConnect", then the 
    value is a list of scope names required for the execution, and the list MAY be empty if 
    authorization does not require a specified scope. For other security scheme types, the array 
    MUST be empty.
    """

    servers: list[OpenApiServer] = field(default_factory=list)
    """
    An alternative server array to service this operation. If an alternative server object is 
    specified at the Path Item Object or Root level, it will be overridden by this value.
    """

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

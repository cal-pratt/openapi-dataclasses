from dataclasses import dataclass, field
from typing import Any, Optional

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config

from .server import OpenApiServer


@dataclass
class OpenApiLink(DataClassJsonMixin):
    """
    The Link object represents a possible design-time link for a response. The presence of a link
    does not guarantee the caller's ability to successfully invoke it, rather it provides a known
    relationship and traversal mechanism between responses and other operations.

    Unlike dynamic links (i.e. links provided in the response payload), the OAS linking mechanism
    does not require link information in the runtime response.

    For computing links, and providing instructions to execute them, a runtime expression is used
    for accessing values in an operation and using them as parameters while invoking the linked
    operation.
    """

    operation_ref: Optional[str] = field(
        metadata=config(field_name="operationRef"), default=None
    )
    """
    A relative or absolute URI reference to an OAS operation. This field is mutually exclusive of
    the operationId field, and MUST point to an Operation Object. Relative operationRef values MAY
    be used to locate an existing Operation Object in the OpenAPI definition.
    """

    operation_id: Optional[str] = field(
        metadata=config(field_name="operationId"), default=None
    )
    """
    The name of an existing, resolvable OAS operation, as defined with a unique operationId. This
    field is mutually exclusive of the operationRef field.
    """

    parameters: dict[str, Any] = field(default_factory=dict)
    """
    A map representing parameters to pass to an operation as specified with operationId or
    identified via operationRef. The key is the parameter name to be used, whereas the value can be
    a constant or an expression to be evaluated and passed to the linked operation. The parameter
    name can be qualified using the parameter location [{in}.]{name} for operations that use the
    same parameter name in different locations (e.g. path.id).
    """

    request_body: Any = field(metadata=config(field_name="requestBody"), default=None)
    """
    A literal value or {expression} to use as a request body when calling the target operation.
    """

    description: Optional[str] = None
    """
    A description of the link. CommonMark syntax MAY be used for rich text representation.
    """

    server: Optional[OpenApiServer] = None
    """
    A server object to be used by the target operation.
    """

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

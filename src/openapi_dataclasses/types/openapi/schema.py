"""
Documentation for this schema layout is defined from:
https://datatracker.ietf.org/doc/html/draft-wright-json-schema-validation-00

Not all features of OpenAPI have been modeled, if you have more use-cases, please create a PR.
"""

from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional, Union

from dataclasses_json import CatchAll, DataClassJsonMixin, Undefined, config


@dataclass
class OpenApiSchema(DataClassJsonMixin):
    """
    JSON Schema (application/schema+json) has several purposes, one of which is JSON instance
    validation. This document specifies a vocabulary for JSON Schema to describe the meaning of
    JSON documents, provide hints for user interfaces working with JSON data, and to make
    assertions about what a valid document must look like.
    """

    enum: Optional[list[Any]] = None
    """5.20.

    The value of this keyword MUST be an array.  This array SHOULD have at least one element. 
    Elements in the array SHOULD be unique.

    Elements in the array MAY be of any type, including null.

    An instance validates successfully against this keyword if its value is equal to one of the 
    elements in this keyword's array value.
    """

    type: list[str] = field(
        metadata=config(
            decoder=lambda d: None if d is None else ([d] if isinstance(d, str) else d),
        ),
        default_factory=list,
    )
    """5.21.

    The value of this keyword MUST be either a string or an array.  If it is an array, elements of 
    the array MUST be strings and MUST be unique.
    
    String values MUST be one of the seven primitive types defined by the core specification.
    
    An instance matches successfully if its primitive type is one of the types defined by keyword. 
    Recall: "number" includes "integer".
    """

    items: list["OpenApiSchema"] = field(
        metadata=config(
            decoder=lambda d: [OpenApiSchema.from_dict(d)]
            if isinstance(d, dict)
            else [OpenApiSchema.from_dict(v) for v in d],
        ),
        default_factory=list,
    )
    additional_items: Optional[Union["OpenApiSchema", bool]] = field(
        metadata=config(
            field_name="additionalItems",
            decoder=lambda d: OpenApiSchema.from_dict(d) if isinstance(d, dict) else d,
        ),
        default=None,
    )
    """5.9.

    The value of "additionalItems" MUST be either a boolean or an object.
    If it is an object, this object MUST be a valid JSON Schema.
    
    The value of "items" MUST be either a schema or array of schemas.
    
    Successful validation of an array instance with regards to these two keywords is determined as
    follows:

        if "items" is not present, or its value is an object, validation of the instance always 
        succeeds, regardless of the value of "additionalItems";
        
        if the value of "additionalItems" is boolean value true or an object, validation of the 
        instance always succeeds;
        
        if the value of "additionalItems" is boolean value false and the value of "items" is an 
        array, the instance is valid if its size is less than, or equal to, the size of "items".

    If either keyword is absent, it may be considered present with an empty schema.
    """

    format: Optional[str] = None
    """7.1.

    Structural validation alone may be insufficient to validate that an instance meets all the 
    requirements of an application. The "format" keyword is defined to allow interoperable semantic
    validation for a fixed subset of values which are accurately described by authoritative 
    resources, be they RFCs or other external specifications.
    
    The value of this keyword is called a format attribute.  It MUST be a string. A format attribute
    can generally only validate a given set of instance types.  If the type of the instance to 
    validate is not in this set, validation for this format attribute and instance SHOULD succeed.
    """

    nullable: bool = False
    """https://swagger.io/specification/

    A true value adds "null" to the allowed type specified by the type keyword, only if type is 
    explicitly defined within the same Schema Object. Other Schema Object constraints retain their 
    defined behavior, and therefore may disallow the use of null as a value. A false value leaves
    the specified or default type unmodified. The default value is false.
    """

    ref: Optional[str] = field(metadata=config(field_name="$ref"), default=None)
    """7.

    Any time a subschema is expected, a schema may instead use an object containing a "$ref" 
    property. The value of the $ref is a URI Reference. Resolved against the current URI base, it 
    identifies the URI of a schema to use. All other properties in a "$ref" object MUST be ignored.
    """

    description: Optional[str] = None
    """https://swagger.io/specification/

    CommonMark syntax MAY be used for rich text representation.
    """

    properties: dict[str, "OpenApiSchema"] = field(
        metadata=config(
            decoder=lambda d: {k: OpenApiSchema.from_dict(d[k]) for k in (d or {})}
        ),
        default_factory=dict,
    )
    """5.16.

    The value of "properties" MUST be an object.  Each value of this object MUST be an object, and 
    each object MUST be a valid JSON Schema.

    If absent, it can be considered the same as an empty object.
    """

    additional_properties: Optional[Union["OpenApiSchema", bool]] = field(
        metadata=config(
            field_name="additionalProperties",
            decoder=lambda d: OpenApiSchema.from_dict(d) if isinstance(d, dict) else d,
        ),
        default=None,
    )
    """5.18.

    The value of "additionalProperties" MUST be a boolean or a schema.
    
    If "additionalProperties" is absent, it may be considered present with an empty schema as a 
    value.
    
    If "additionalProperties" is true, validation always succeeds.
    
    If "additionalProperties" is false, validation succeeds only if the instance is an object and
    all properties on the instance were covered by "properties" and/or "patternProperties".
    
    If "additionalProperties" is an object, validate the value as a schema to all of the properties
    that weren't validated by "properties" nor "patternProperties".
    """

    dataclass_json_config = config(undefined=Undefined.INCLUDE)["dataclasses_json"]  # type: ignore
    unhandled_data: CatchAll = field(default_factory=dict)

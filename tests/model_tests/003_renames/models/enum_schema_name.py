from enum import Enum


class EnumSchemaName(Enum):
    ONE = "one"
    TWO_TWO = "TwoTwo"
    THREE = "THREE"

    def __repr__(self):
        return self.value

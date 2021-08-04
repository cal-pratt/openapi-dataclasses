from enum import Enum


class EnumSchema(Enum):
    ONE = "one"
    TWO = "two"
    THREE = "three"

    def __repr__(self):
        return self.value

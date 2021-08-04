from enum import Enum


class EnumClass(Enum):
    FOO = "foo"

    def __repr__(self):
        return self.value

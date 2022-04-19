#  -*- coding: utf-8 -*-

from enum import Enum
from typing import Any, TypeVar

_StrEnumT = TypeVar("_StrEnumT", bound="StrEnum")


class StrEnum(str, Enum):
    """
    Enum where members are also (and must be) strings
    """

    def __new__(cls: type[_StrEnumT], *values: Any, **kwargs: Any) -> _StrEnumT:
        if len(values) > 3:
            raise TypeError(f"too many arguments for str(): {values!r}")
        if len(values) == 1:
            # it must be a string
            if not isinstance(values[0], str):
                raise TypeError(f"{values[0]!r} is not a string")
        if len(values) >= 2:
            # check that encoding argument is a string
            if not isinstance(values[1], str):
                raise TypeError("encoding must be a string, not {values[1]!r}")
        if len(values) == 3:
            # check that error's argument is a string
            if not isinstance(values[2], str):
                raise TypeError(f"errors must be a string, not {values[2]!r}")
        value = str(*values)
        member = str.__new__(cls, value)
        member._value_ = value
        return member

    __str__ = str.__str__

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> str:
        """
        Return the lower-cased version of the member name.
        """
        return name.lower()

#  -*- coding: utf-8 -*-

import re
from collections.abc import Callable, Iterable, KeysView, Mapping
from datetime import datetime
from typing import Any, TypeVar

import slugify as unicode_slug

from .dt import as_local

_T = TypeVar("_T")
_U = TypeVar("_U")

RE_SANITIZE_FILENAME = re.compile(r"(~|\.\.|/|\\)")
RE_SANITIZE_PATH = re.compile(r"(~|\.(\.)+)")


def raise_if_invalid_filename(filename: str) -> None:
    """
    Check if a filename is valid.
    Raises a ValueError if the filename is invalid.
    """
    if RE_SANITIZE_FILENAME.sub("", filename) != filename:
        raise ValueError(f"{filename} is not a safe filename")


def raise_if_invalid_path(path: str) -> None:
    """
    Check if a path is valid.
    Raises a ValueError if the path is invalid.
    """
    if RE_SANITIZE_PATH.sub("", path) != path:
        raise ValueError(f"{path} is not a safe path")


def slugify(text: str | None, *, separator: str = "_") -> str:
    """Slugify a given text."""
    if text == "" or text is None:
        return ""
    slug = unicode_slug.slugify(text, separator=separator)
    return "unknown" if slug == "" else slug


def repr_helper(inp: Any) -> str:
    """Help creating a more readable string representation of objects."""
    if isinstance(inp, Mapping):
        return ", ".join(f"{repr_helper(key)}={repr_helper(item)}" for key, item in inp.items())
    if isinstance(inp, datetime):
        return as_local(inp).isoformat()

    return str(inp)


def convert(value: _T | None, to_type: Callable[[_T], _U], default: _U | None = None) -> _U | None:
    """Convert value to to_type, returns default if fails."""
    try:
        return default if value is None else to_type(value)
    except (ValueError, TypeError):
        # If value could not be converted
        return default


def ensure_unique_string(
    preferred_string: str, current_strings: Iterable[str] | KeysView[str]
) -> str:
    """Return a string that is not present in current_strings.
    If preferred string exists will append _2, _3, ..
    """
    test_string = preferred_string
    current_strings_set = set(current_strings)

    tries = 1

    while test_string in current_strings_set:
        tries += 1
        test_string = f"{preferred_string}_{tries}"

    return test_string

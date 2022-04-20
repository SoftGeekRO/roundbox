#  -*- coding: utf-8 -*-

import logging
import os
from pprint import pformat
from typing import IO, Any, Literal, Mapping, Optional

from RoundBox.core.cliparser.color import color_style
from RoundBox.utils.log.filters import PasswordMaskingFilter

from . import themes
from .color import (
    ColoredRecord,
    EscapeCodes,
    LogColors,
    SecondaryLogColors,
    default_log_colors,
    escape_codes,
    parse_colors,
)

# The default format to use for each style
default_formats = {
    "%": "%(log_color)s%(levelname)s:%(name)s:%(message)s",
    "{": "{log_color}{levelname}:{name}:{message}",
    "$": "${log_color}${levelname}:${name}:${message}",
}


class ServerFormatter(logging.Formatter):
    default_time_format = '%d/%b/%Y %H:%M:%S'

    def __init__(self, *args, **kwargs):
        self.style = color_style()
        super().__init__(*args, **kwargs)

    def format(self, record):
        msg = record.msg

        if self.uses_server_time() and not hasattr(record, 'server_time'):
            record.server_time = self.formatTime(record, self.datefmt)

        record.msg = msg
        return super().format(record)

    def uses_server_time(self):
        return self._fmt.find('{server_time}') >= 0


class PrivacyFormatter(logging.Formatter):
    def format(self, record):
        res = super().format(record)

        if hasattr(record, 'request'):
            filtered_request = PasswordMaskingFilter.sanitize_dict(record.request)
            res += '\n\t' + pformat(filtered_request, indent=4).replace('\n', '\n\t')
        return res


class ColoredFormatter(logging.Formatter):
    """Special custom formatter for colorizing log messages!"""

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%",
        log_colors: Optional[LogColors] = None,
        reset: bool = True,
        secondary_log_colors: Optional[SecondaryLogColors] = None,
        validate: bool = True,
        stream: Optional[IO] = None,
        no_color: bool = False,
        force_color: bool = False,
        icons=None,
        icon_style='rounded',
    ) -> None:
        """Set the format and colors the ColoredFormatter will use.

        The ``fmt``, ``datefmt`` and ``style`` args are passed on to the
        ``logging.Formatter`` constructor.

        The ``secondary_log_colors`` argument can be used to create additional
        ``log_color`` attributes. Each key in the dictionary will set
        ``{key}_log_color``, using the value to select from a different
        ``log_colors`` set.

        :param fmt: The format string to use.
        :param datefmt: A format string for the date.
        :param style: The format style to use. (*No meaning prior to Python 3.2.*)
        :param log_colors: A mapping of log level names to color names.
        :param reset: A mapping of log level names to color names.
        :param secondary_log_colors: Map secondary ``log_color`` attributes. (*New in version 2.6.*)
        :param validate: Validate the format string.
        :param stream: The stream formatted messages will be printed to. Used to toggle colour
            on non-TTY outputs. Optional.
        :param no_color: Disable color output.
        :param force_color: Enable color output. Takes precedence over `no_color`.
        :param icons: dict of level:value for icons
        :param icons_style: str
        """

        # Select a default format if `fmt` is not provided.
        fmt = default_formats[style] if fmt is None else fmt

        super().__init__(fmt, datefmt, style, validate)

        self.log_colors = log_colors if log_colors is not None else default_log_colors
        self.secondary_log_colors = (
            secondary_log_colors if secondary_log_colors is not None else {}
        )
        self.reset = reset
        self.stream = stream
        self.no_color = no_color
        self.force_color = force_color

        self.icon_style = icon_style
        self.theme_icons = icons if icons else themes.icons.get(self.icon_style)

        self.fmt = fmt
        self.fmt = style

    @property
    def is_tty(self):
        """

        :return:
        """
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def formatMessage(self, record: logging.LogRecord) -> str:
        """Format a message from a record object.

        :param record:
        :return:
        """
        levelname = record.levelname  # len7 limit

        if levelname == 'CRITICAL':
            levelname = record.levelname = 'FATAL'

        record.icon = self.theme_icons.get(levelname, '')

        escapes = self._escape_code_map(levelname)
        wrapper = ColoredRecord(record, escapes)
        message = super().formatMessage(wrapper)  # type: ignore
        message = self._append_reset(message, escapes)
        return message

    def _escape_code_map(self, item: str) -> EscapeCodes:
        """Build a map of keys to escape codes for use in message formatting.
        If _blank_escape_codes() returns True, all values will be an empty string.

        :param item:
        :return:
        """
        codes = {**escape_codes}
        codes.setdefault("log_color", self._get_escape_code(self.log_colors, item))
        for name, colors in self.secondary_log_colors.items():
            codes.setdefault("%s_log_color" % name, self._get_escape_code(colors, item))
        if self._blank_escape_codes():
            codes = {key: "" for key in codes.keys()}
        return codes

    def _blank_escape_codes(self):
        """Return True if we should be prevented from printing escape codes.

        :return:
        """
        if self.force_color or "FORCE_COLOR" in os.environ:
            return False

        if self.no_color or "NO_COLOR" in os.environ:
            return True

        if self.stream is not None and not self.stream.isatty():
            return True

        return False

    @staticmethod
    def _get_escape_code(log_colors: LogColors, item: str) -> str:
        """Extract a color sequence from a mapping, and return escape codes.

        :param log_colors:
        :param item:
        :return:
        """
        return parse_colors(log_colors.get(item, ""))

    def _append_reset(self, message: str, escapes: EscapeCodes) -> str:
        """Add a reset code to the end of the message, if it's not already there.

        :param message:
        :param escapes:
        :return:
        """
        reset_escape_code = escapes["reset"]

        if self.reset and not message.endswith(reset_escape_code):
            message += reset_escape_code

        return message


class LevelFormatter:
    """An extension of ColoredFormatter that uses per-level format strings."""

    def __init__(self, fmt: Mapping[str, str], **kwargs: Any) -> None:
        """Configure a ColoredFormatter with its own format string for each log level.
        Supports fmt as a dict. All other args are passed on to the
        ``colorlog.ColoredFormatter`` constructor.
        :Parameters:
        - fmt (dict):
            A mapping of log levels (represented as strings, e.g. 'WARNING') to
            format strings. (*New in version 2.7.0)
        (All other parameters are the same as in colorlog.ColoredFormatter)
        Example:
        formatter = colorlog.LevelFormatter(
            fmt={
                "DEBUG": "%(log_color)s%(message)s (%(module)s:%(lineno)d)",
                "INFO": "%(log_color)s%(message)s",
                "WARNING": "%(log_color)sWRN: %(message)s (%(module)s:%(lineno)d)",
                "ERROR": "%(log_color)sERR: %(message)s (%(module)s:%(lineno)d)",
                "CRITICAL": "%(log_color)sCRT: %(message)s (%(module)s:%(lineno)d)",
            }
        )

        :param fmt:
        :param kwargs:
        """
        self.formatters = {level: ColoredFormatter(fmt=f, **kwargs) for level, f in fmt.items()}

    def format(self, record: logging.LogRecord) -> str:
        return self.formatters[record.levelname].format(record)

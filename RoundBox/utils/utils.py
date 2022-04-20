#  -*- coding: utf-8 -*-

import argparse
import pathlib
import re
import sys
import textwrap
from argparse import ArgumentParser, Namespace
from functools import lru_cache
from importlib import import_module

import pkg_resources

from RoundBox.const import REQUIRED_PYTHON_VER, __version__


def load_arguments() -> tuple[ArgumentParser, tuple[Namespace, list[str]]]:
    """Load arguments used in shell instance
    :return: An objects with argument name properties
    """
    parser = argparse.ArgumentParser(
        prog='RoundBox',
        description="Small framework inspired by Django and Home Assistant used for IoT device parser.",
        epilog="For more information read the documentation",
    )

    parser.add_argument("--debug", type=bool, default=False, help="RoundBox in debug mode")

    parser.add_argument(
        '--auth-type', type=str, default=None, help="Authentication type on the API service"
    )
    parser.add_argument("--username", type=str, default="", help="Growatt username account")
    parser.add_argument("--password", type=str, default="", help="Growatt password account")
    parser.add_argument("--api-key-token", type=str, default="", help="Growatt API KEY TOKEN")
    parser.add_argument(
        "--plant-id",
        type=int,
        default=0,
        help="ID of the plant that you want to get the " "information",
    )
    parser.add_argument("--user-id", type=int, default=None, help="ID of the logged user")
    parser.add_argument(
        "--inverter-id",
        type=list,
        nargs="+",
        help="List of you Growatt inverters, delimited by space",
    )

    parser.add_argument("--owm-key", type=str, default="", help="API key from Open Weather Map")
    parser.add_argument(
        "--owm-lat", type=float, default=0.0, help="Latitude location for Open Weather Map"
    )
    parser.add_argument(
        "--owm-lon", type=float, default=0.0, help="Longitude location for Open Weather Map"
    )

    parser.add_argument("--pv-output-key", type=str, default="", help="API Key from PVOutput")
    parser.add_argument(
        "--pv-output-system-id", type=int, default=0, help="System ID from PVOutput"
    )

    parser.add_argument(
        "--influxdb-url", type=str, default="http://localhost:8086", help="InfluxDB URL path"
    )
    parser.add_argument("--influxdb-token", type=str, default="my-token", help="InfluxDB token")
    parser.add_argument("--influxdb-org", type=str, default="my-org", help="Influxdb organization")

    parser.add_argument(
        "--ignore-os-check", action="store_true", help="Skips validation of operating system"
    )

    parser.add_argument(
        "--skip-dependency",
        action="store_true",
        help="Skips checks of required packages on startup",
    )

    parser.add_argument('--version', action='version', version=__version__)

    return parser, parser.parse_known_args()


def import_string(dotted_path):
    """Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class' % (module_path, class_name)
        ) from err


def format_multi_line(prefix, string, size=80) -> str:
    """Formats multi-line data

    :param prefix:
    :param string:
    :param size:
    :return:
    """
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])


@lru_cache
def read_requirements() -> dict:
    """

    :return:
    """

    try:
        with pathlib.Path('requirements.txt').open(mode='rt', encoding='UTF-8') as f:
            line = f.read().splitlines()

        content = {}
        for kv in line:
            k, v = re.split(r'==|>=', kv)
            content.update({k: v})

        return content
    except IOError:
        return {}


def check_dependency() -> str | None:
    """

    :return:
    """
    installed_packages = {d.project_name: d.version for d in pkg_resources.working_set}
    requirement_list = read_requirements()

    missing_packages = set(requirement_list.items()) - set(installed_packages.items())
    if missing_packages:
        package = ", ".join(f"{package}({_})" for package, _ in missing_packages)
        return package
    return None


def validate_os() -> bool:
    """Validate that RoundBox is running in a supported operating system.

    :return:
    """

    """"""
    return sys.platform.startswith(("darwin", "linux"))


def validate_python() -> tuple[tuple, tuple[int, int, int]] | tuple[None, None]:
    """Validate that the right Python version is running."""
    if sys.version_info[:3] < REQUIRED_PYTHON_VER:
        return sys.version_info[:3], REQUIRED_PYTHON_VER

    return None, None

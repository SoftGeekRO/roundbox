#  -*- coding: utf-8 -*-

from RoundBox.conf.project_settings import settings
from RoundBox.utils.utils import check_dependency, validate_os, validate_python

from . import Error, Tags, register


@register(Tags.runtime)
def check_dependency_packages(app_configs, **kwargs):
    """

    :param app_configs:
    :param kwargs:
    :return:
    """
    packages = check_dependency()

    if packages:
        return [
            Error(
                f"To run the RoundBox you must install the fallowing packages: {packages} ",
                _id="runtime.E001",
            ),
        ]

    return []


@register(Tags.runtime)
def check_validate_os(app_configs, **kwargs):
    """

    :param app_configs:
    :param kwargs:
    :return:
    """
    if not validate_os():
        return [
            Error(
                f"To use this framework you have to run it from a Linux distribution",
                _id="runtime.E001",
            ),
        ]

    return []


@register(Tags.runtime)
def check_python_version(app_configs, **kwargs):
    """

    :param app_configs:
    :param kwargs:
    :return:
    """
    sys_python, required_python = validate_python()

    if sys_python:
        sys_python = '.'.join(map(str, sys_python))
        required_python = '.'.join(map(str, required_python))
        return [
            Error(
                f"RoundBox requires at least Python {required_python} and you you have: {sys_python}",
                _id="runtime.E001",
            ),
        ]

    return []

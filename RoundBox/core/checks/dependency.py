#  -*- coding: utf-8 -*-
#
#  Copyright (C) 2020-2022 ProGeek
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from RoundBox.conf.project_settings import settings
from RoundBox.utils.utils import validate_os, validate_python, check_dependency

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
                f"To run the RoundBox you must install the fallowing packages: {packages} ", _id="runtime.E001",
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
                f"To use this framework you have to run it from a Linux distribution", _id="runtime.E001",
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

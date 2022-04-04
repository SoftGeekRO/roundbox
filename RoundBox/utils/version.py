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

from RoundBox.utils.regex_helper import _lazy_re_compile

version_component_re = _lazy_re_compile(r"(\d+|[a-z]+|\.)")


def get_version_tuple(version):
    """Return a tuple of version numbers (e.g. (1, 2, 3)) from the version
    string (e.g. '1.2.3').

    :param version:
    :return:
    """
    version_numbers = []
    for item in version_component_re.split(version):
        if item and item != ".":
            try:
                component = int(item)
            except ValueError:
                break
            else:
                version_numbers.append(component)
    return tuple(version_numbers)

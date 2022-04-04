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

import hashlib

from RoundBox.utils.inspect import func_supports_parameter


if func_supports_parameter(hashlib.md5, "usedforsecurity"):
    md5 = hashlib.md5
    new_hash = hashlib.new
else:

    def md5(data=b"", *, usedforsecurity=True):
        return hashlib.md5(data)

    def new_hash(hash_algorithm, *, usedforsecurity=True):
        return hashlib.new(hash_algorithm)

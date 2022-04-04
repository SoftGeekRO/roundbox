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

from RoundBox.core.cache.backends.base import DEFAULT_TIMEOUT, BaseCache


class DummyCache(BaseCache):
    def __init__(self, host, *args, **kwargs):
        """Dummy cache backend

        :param host:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        self.make_and_validate_key(key, version=version)
        return True

    def get(self, key, default=None, version=None):
        self.make_and_validate_key(key, version=version)
        return default

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        self.make_and_validate_key(key, version=version)

    def touch(self, key, timeout=DEFAULT_TIMEOUT, version=None):
        self.make_and_validate_key(key, version=version)
        return False

    def delete(self, key, version=None):
        self.make_and_validate_key(key, version=version)
        return False

    def has_key(self, key, version=None):
        self.make_and_validate_key(key, version=version)
        return False

    def clear(self):
        pass

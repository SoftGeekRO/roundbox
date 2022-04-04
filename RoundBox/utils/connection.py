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

from asgiref.local import Local

from RoundBox.conf.project_settings import settings as django_settings
from RoundBox.utils.functional import cached_property


class ConnectionProxy:

    def __init__(self, connections, alias):
        """Proxy for accessing a connection object's attributes.

        :param connections:
        :param alias:
        """
        self.__dict__["_connections"] = connections
        self.__dict__["_alias"] = alias

    def __getattr__(self, item):
        return getattr(self._connections[self._alias], item)

    def __setattr__(self, name, value):
        return setattr(self._connections[self._alias], name, value)

    def __delattr__(self, name):
        return delattr(self._connections[self._alias], name)

    def __contains__(self, key):
        return key in self._connections[self._alias]

    def __eq__(self, other):
        return self._connections[self._alias] == other


class ConnectionDoesNotExist(Exception):
    pass


class BaseConnectionHandler:
    settings_name = None
    exception_class = ConnectionDoesNotExist
    thread_critical = False

    def __init__(self, settings=None):
        self._settings = settings
        self._connections = Local(self.thread_critical)

    @cached_property
    def settings(self):
        self._settings = self.configure_settings(self._settings)
        return self._settings

    def configure_settings(self, settings):
        if settings is None:
            settings = getattr(django_settings, self.settings_name)
        return settings

    def create_connection(self, alias):
        raise NotImplementedError("Subclasses must implement create_connection().")

    def __getitem__(self, alias):
        try:
            return getattr(self._connections, alias)
        except AttributeError:
            if alias not in self.settings:
                raise self.exception_class(f"The connection '{alias}' doesn't exist.")
        conn = self.create_connection(alias)
        setattr(self._connections, alias, conn)
        return conn

    def __setitem__(self, key, value):
        setattr(self._connections, key, value)

    def __delitem__(self, key):
        delattr(self._connections, key)

    def __iter__(self):
        return iter(self.settings)

    def all(self, initialized_only=False):
        return [
            self[alias]
            for alias in self
            # If initialized_only is True, return only initialized connections.
            if not initialized_only or hasattr(self._connections, alias)
        ]

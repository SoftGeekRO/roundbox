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


# Caching framework.
# This package defines set of cache backends that all conform to a simple API.
# In a nutshell, a cache is a set of values -- which can be any object that
# may be pickled -- identified by string keys.  For the complete API, see
# the abstract BaseCache class in django.core.cache.backends.base.
# Client code should use the `cache` variable defined here to access the default
# cache backend and look up non-default cache backends in the `caches` dict-like
# object.
#
# inspired by Django cache framework
# https://github.com/django/django/tree/main/django/core/cache


from RoundBox.core import signals
from RoundBox.core.cache.backends.base import (
    BaseCache,
    CacheKeyWarning,
    InvalidCacheBackendError,
    InvalidCacheKey,
)
from RoundBox.utils.connection import BaseConnectionHandler, ConnectionProxy
from RoundBox.utils.module_loading import import_string

from RoundBox.utils.module_loading import import_string

__all__ = [
    "cache",
    "caches",
    "DEFAULT_CACHE_ALIAS",
    "InvalidCacheBackendError",
    "CacheKeyWarning",
    "BaseCache",
    "InvalidCacheKey",
]

DEFAULT_CACHE_ALIAS = "default"


class CacheHandler(BaseConnectionHandler):
    settings_name = "CACHES"
    exception_class = InvalidCacheBackendError

    def create_connection(self, alias):
        params = self.settings[alias].copy()

        backend = params.pop("BACKEND")
        location = params.pop("LOCATION", "")
        try:
            backend_cls = import_string(backend)
        except ImportError as e:
            raise InvalidCacheBackendError(
                "Could not find backend '%s': %s" % (backend, e)
            ) from e
        return backend_cls(location, params)


caches = CacheHandler()

cache = ConnectionProxy(caches, DEFAULT_CACHE_ALIAS)


def close_caches(**kwargs):
    # Some caches need to do a cleanup at the end of a request cycle. If not
    # implemented in a particular backend cache.close() is a no-op.
    for cache in caches.all(initialized_only=True):
        cache.close()


signals.request_finished.connect(close_caches)

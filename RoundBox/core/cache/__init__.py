#  -*- coding: utf-8 -*-

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
            raise InvalidCacheBackendError("Could not find backend '%s': %s" % (backend, e)) from e
        return backend_cls(location, params)


caches = CacheHandler()

cache = ConnectionProxy(caches, DEFAULT_CACHE_ALIAS)


def close_caches(**kwargs):
    # Some caches need to do a cleanup at the end of a request cycle. If not
    # implemented in a particular backend cache.close() is a no-op.
    for cache in caches.all(initialized_only=True):
        cache.close()


signals.request_finished.connect(close_caches)

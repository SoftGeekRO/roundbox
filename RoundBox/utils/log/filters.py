#  -*- coding: utf-8 -*-

import logging
import time
from hashlib import md5

from RoundBox.conf.project_settings import settings
from RoundBox.core.cache import cache


class RequireDebugFalse(logging.Filter):
    def filter(self, records):
        return not settings.DEBUG


class RequireDebugTrue(logging.Filter):
    def filter(self, record):
        return settings.DEBUG


class RateLimiterFilter(logging.Filter):
    def filter(self, record):
        """

        :param record:
        :return:
        """
        # Rate is specified as 1 messages logged per N seconds. (aka cache timeout)
        rate = getattr(settings, 'RATE_LIMITER_FILTER_RATE', 10)
        prefix = getattr(settings, 'RATE_LIMITER_FILTER_PREFIX', 'ratelimiterfilter')

        subject = record.getMessage()
        cache_key = "%s:%s" % (prefix, md5(subject.encode('utf-8')).hexdigest())
        cache_count_key = "%s:count" % cache_key

        result = cache.get_many([cache_key, cache_count_key])
        value = result.get(cache_key)
        cntr = result.get(cache_count_key)

        if not cntr:
            cntr = 1
            cache.set(cache_count_key, cntr, rate + 60)

        if value:
            cache.incr(cache_count_key)
            return False

        record.msg = "[%sx] %s" % (cntr, record.msg)
        cache.set(cache_key, time.time(), rate)
        return True


class PasswordMaskingFilter(logging.Filter):
    """Filter and mask the password values from dictionary that are listed in log"""

    def filter(self, record) -> bool:
        """The call signature matches string interpolation: args can be a tuple or a lone dict

        :param record:
        :return:
        """
        if isinstance(record.args, dict):
            record.args = self.sanitize_dict(record.args)
        else:
            record.args = tuple(self.sanitize_dict(i) for i in record.args)

        return True

    @staticmethod
    def sanitize_dict(d) -> dict:
        """

        :param d:
        :return:
        """
        if not isinstance(d, dict):
            return d

        if any(i for i in d.keys() if 'password' in i):
            d = d.copy()  # Ensure that we won't clobber anything critical

            for k, v in d.items():
                if 'password' in k:
                    d[k] = '*** PASSWORD ***'

        return d

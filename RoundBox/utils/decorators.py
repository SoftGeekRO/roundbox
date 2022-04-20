#  -*- coding: utf-8 -*-

import functools

from loguru import logger

from RoundBox.conf.project_settings import settings


def logger_wraps(*args, **kwargs):
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*_args, **_kwargs):
            logger_ = logger.opt(depth=1)
            if settings.DEBUG:
                logger_.debug("Entering '{}' (args={}, kwargs={})", name, _args, _kwargs)
            result = func(*_args, **_kwargs)
            if settings.DEBUG:
                logger_.debug("Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper

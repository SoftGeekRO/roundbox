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

import os
import sys
from threading import RLock
import logging
import logging.config


from RoundBox.utils.utils import import_string


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'RoundBox.utils.log.filters.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'RoundBox.utils.log.filters.RequireDebugTrue',
        },
        'ratelimit': {
            '()': 'RoundBox.utils.log.filters.RateLimiterFilter',
        },
        'privacy': {
            '()': 'RoundBox.utils.log.filters.PasswordMaskingFilter'
        }
    },
    'formatters': {
        'RoundBox.server': {
            '()': 'RoundBox.utils.log.formatter.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'console.info': {
            '()': 'RoundBox.utils.log.formatter.ColoredFormatter',
            'format': u'{log_color}{icon:<2s}{levelname: <7s} {module}.{funcName}:{lineno:d}{reset} '
                      '{message}',
            'style': '{',
            'icon_style': 'symbol'
        },
        'console.debug': {
            '()': 'RoundBox.utils.log.formatter.ColoredFormatter',
            'format': u'{log_color}{icon:<2s}{levelname: <7s} {asctime} {module}.{funcName}:{lineno:d}{reset} '
                      '{message}',
            'style': '{',
            'icon_style': 'symbol'
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        # 'privacy': {
        #     '()': 'RoundBox.utils.log.PrivacyFormatter',
        #     'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
        #     'style': '{'
        # }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
            'filename': 'log/debug.log',
            'encoding': 'utf8',
            'formatter': 'verbose',
            'filters': ['require_debug_true', 'privacy'],
        },
        'stdout': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'console.debug',
            "stream": "ext://sys.stdout",
            'filters': ['require_debug_true', 'ratelimit', 'privacy'],
        },
        'stderr': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'console.info',
            "stream": "ext://sys.stderr",
            'filters': ['require_debug_false', 'privacy'],
        },
    },
    'loggers': {
        'growatt_logging': {
            'handlers': ['stderr', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'dispatch': {
            'handlers': ['stderr', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'file': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'schedule': {
            'handlers': ['stderr', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {'level': 'NOTSET', 'handlers': ['stderr', 'stdout', 'file']},
}


def configure_logging(logging_config, logging_settings):
    """

    :param logging_config:
    :param logging_settings:
    :return:
    """
    if logging_config:
        # First find the logging configuration function ...
        logging_config_func = import_string(logging_config)

        logging.config.dictConfig(DEFAULT_LOGGING)

        # ... then invoke it with the logging settings
        if logging_settings:
            logging_config_func(logging_settings)

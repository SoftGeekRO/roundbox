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
#
# inspired by django_extensions package management commands:
# https://github.com/django-extensions/django-extensions
# https://github.com/django-extensions/django-extensions/blob/main/django_extensions/management/commands/print_settings.py
# inspired by django_extensions package management commands:
# https://github.com/django-extensions/django-extensions
# https://github.com/django-extensions/django-extensions/blob/main/django_extensions/management/commands/print_settings.py

import fnmatch
import json

from RoundBox.conf.project_settings import settings
from RoundBox.core.cliparser.base import BaseCommand, CommandError

from RoundBox.core.cliparser.utils import signalcommand


class Command(BaseCommand):
    help = "Print the active RoundBox settings."

    def add_arguments(self, parser) -> None:
        """

        :param parser:
        :return:
        """
        super().add_arguments(parser)
        parser.add_argument('setting', nargs='*', help='Specifies setting to be printed.')
        parser.add_argument(
            '-f',
            '--fail',
            action='store_true',
            dest='fail',
            help='Fail if invalid setting name is given.',
        )
        parser.add_argument(
            '--format', default='simple', dest='format', help='Specifies output format.'
        )
        parser.add_argument(
            '--indent',
            default=4,
            dest='indent',
            type=int,
            help='Specifies indent level for JSON and YAML',
        )

    @signalcommand
    def handle(self, *args, **options) -> None:
        """

        :param args:
        :param options:
        :return:
        """
        setting_names = options['setting']
        settings_dct = {k: getattr(settings, k) for k in dir(settings) if k.isupper()}

        if setting_names:
            settings_dct = {
                key: value
                for key, value in settings_dct.items()
                if any(fnmatch.fnmatchcase(key, setting_name) for setting_name in setting_names)
            }

        if options['fail']:
            for setting_name in setting_names:
                if not any(fnmatch.fnmatchcase(key, setting_name) for key in settings_dct.keys()):
                    raise CommandError('%s not found in settings.' % setting_name)

        output_format = options['format']
        indent = options['indent']

        match output_format:
            case 'json':
                print(json.dumps(settings_dct, indent=indent))
            case 'yaml':
                import yaml  # requires PyYAML

                print(yaml.dump(settings_dct, indent=indent))
            case 'pprint':
                from pprint import pprint

                pprint(settings_dct)
            case 'text':
                for key, value in settings_dct.items():
                    print("%s = %s" % (key, value))
            case 'value':
                for value in settings_dct.values():
                    print(value)
            case _:
                for key, value in settings_dct.items():
                    print('%-40s = %r' % (key, value))

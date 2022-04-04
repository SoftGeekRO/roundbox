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
# https://github.com/django-extensions/django-extensions/blob/main/django_extensions/management/commands/clean_pyc.py

import fnmatch
import os
from os.path import join as _j

from RoundBox.conf.project_settings import settings
from RoundBox.core.cliparser.base import BaseCommand, CommandError

from RoundBox.core.cliparser.utils import signalcommand


class Command(BaseCommand):
    help = "Removes all python bytecode compiled files from the project."

    requires_system_checks = []

    def add_arguments(self, parser) -> None:
        """

        :param parser:
        :return:
        """
        parser.add_argument(
            '--optimize', '-o', '-O', action='store_true',
            dest='optimize', default=False,
            help='Remove optimized python bytecode files'
        )
        parser.add_argument(
            '--path', '-p', action='store', dest='path',
            help='Specify path to recurse into'
        )

    @signalcommand
    def handle(self, *args, **options) -> None:
        """

        :param args:
        :param options:
        :return:
        """
        project_root = options.get("path", getattr(settings, 'BASE_DIR', None))
        if not project_root:
            project_root = getattr(settings, 'BASE_DIR', None)

        verbosity = options["verbosity"]
        if not project_root:
            raise CommandError("No --path specified and settings.py does not contain BASE_DIR")

        exts = options["optimize"] and "*.py[co]" or "*.pyc"

        for root, dirs, filenames in os.walk(project_root):
            for filename in fnmatch.filter(filenames, exts):
                full_path = _j(root, filename)
                if verbosity > 1:
                    self.stdout.write("%s\n" % full_path)
                os.remove(full_path)

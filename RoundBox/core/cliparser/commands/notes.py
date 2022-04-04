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
# https://github.com/django-extensions/django-extensions/blob/main/django_extensions/management/commands/notes.py

import os
import re

from RoundBox.conf.project_settings import settings
from RoundBox.core.cliparser.base import BaseCommand, CommandError

from RoundBox.core.cliparser.utils import signalcommand

ANNOTATION_RE = re.compile(r"\{?#[\s]*?(TODO|FIXME|BUG|HACK|WARNING|NOTE|XXX)[\s:]?(.+)")
ANNOTATION_END_RE = re.compile(r"(.*)#\}(.*)")


class Command(BaseCommand):
    help = 'Show all annotations like TODO, FIXME, BUG, HACK, WARNING, NOTE or XXX in your py and HTML files.'
    label = 'annotation tag (TODO, FIXME, BUG, HACK, WARNING, NOTE, XXX)'

    def add_arguments(self, parser) -> None:
        """

        :param parser:
        :return:
        """

        super().add_arguments(parser)
        parser.add_argument(
            '--tag',
            dest='tag',
            help='Search for specific tags only',
            action='append'
        )

    @signalcommand
    def handle(self, *args, **options) -> None:
        """

        :param args:
        :param options:
        :return:
        """

        # don't add RoundBox internal code
        apps = [app.replace(".", "/") for app in settings.INSTALLED_APPS]
        base_dir = getattr(settings, 'BASE_DIR')
        for app_dir in apps:
            if base_dir:
                app_dir = os.path.join(base_dir, app_dir)

            for top, dirs, files in os.walk(app_dir):
                for fn in files:
                    if os.path.splitext(fn)[1] in ('.py', '.html'):
                        fpath = os.path.join(top, fn)
                        annotation_lines = []
                        with open(fpath, 'r') as fd:
                            i = 0
                            for line in fd.readlines():
                                i += 1
                                if ANNOTATION_RE.search(line):
                                    tag, msg = ANNOTATION_RE.findall(line)[0]
                                    if options['tag']:
                                        if tag not in map(str.upper, map(str, options['tag'])):
                                            break

                                    if ANNOTATION_END_RE.search(msg.strip()):
                                        msg = ANNOTATION_END_RE.findall(msg.strip())[0][0]

                                    annotation_lines.append("[%3s] %-5s %s" % (i, tag, msg.strip()))
                            if annotation_lines:
                                self.stdout.write("%s:" % fpath)
                                for annotation in annotation_lines:
                                    self.stdout.write("  * %s" % annotation)
                                self.stdout.write("")

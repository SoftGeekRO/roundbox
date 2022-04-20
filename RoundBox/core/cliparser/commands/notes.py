#  -*- coding: utf-8 -*-

# Copyright (c) django-extensions
# All rights reserved.
# https://github.com/django-extensions/django-extensions/blob/main/LICENSE

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
            '--tag', dest='tag', help='Search for specific tags only', action='append'
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

                                    annotation_lines.append(
                                        "[%3s] %-5s %s" % (i, tag, msg.strip())
                                    )
                            if annotation_lines:
                                self.stdout.write("%s:" % fpath)
                                for annotation in annotation_lines:
                                    self.stdout.write("  * %s" % annotation)
                                self.stdout.write("")

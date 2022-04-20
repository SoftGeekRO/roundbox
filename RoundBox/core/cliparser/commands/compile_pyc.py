#  -*- coding: utf-8 -*-

# Copyright (c) django-extensions
# All rights reserved.
# https://github.com/django-extensions/django-extensions/blob/main/LICENSE


import fnmatch
import os
import py_compile
from os.path import join as _j

from RoundBox.conf.project_settings import settings
from RoundBox.core.cliparser.base import BaseCommand, CommandError
from RoundBox.core.cliparser.utils import signalcommand


class Command(BaseCommand):
    help = "Compile python bytecode files for the project."

    requires_system_checks = []

    def add_arguments(self, parser) -> None:
        """

        :param parser:
        :return:
        """
        parser.add_argument(
            '--path', '-p', action='store', dest='path', help='Specify path to recurse into'
        )

    @signalcommand
    def handle(self, *args, **options) -> None:
        """

        :param args:
        :param options:
        :return:
        """
        project_root = options["path"]
        if not project_root:
            project_root = getattr(settings, 'BASE_DIR', None)

        verbosity = options["verbosity"]
        if not project_root:
            raise CommandError("No --path specified and settings.py does not contain BASE_DIR")

        for root, dirs, filenames in os.walk(project_root):
            for filename in fnmatch.filter(filenames, '*.py'):
                full_path = _j(root, filename)
                if verbosity > 1:
                    self.stdout.write("Compiling %s...\n" % full_path)
                py_compile.compile(full_path)

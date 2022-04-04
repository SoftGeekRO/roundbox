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
import errno

from RoundBox.conf.project_settings import settings
from RoundBox.core.cliparser.base import BaseCommand, CommandError
from RoundBox.utils import autoreload


class Command(BaseCommand):
    help = "Start the production server with all the active applications"

    def add_arguments(self, parser):
        pass

    def get_handler(self, *args, **options):
        """Return the default WSGI handler for the runner."""
        return None

    def execute(self, *args, **options):
        if options["no_color"]:
            # We rely on the environment because it's currently the only
            # way to reach WSGIRequestHandler. This seems an acceptable
            # compromise considering `runserver` runs indefinitely.
            os.environ["ROUNDBOX_COLORS"] = "nocolor"
        super().execute(*args, **options)

    def handle(self, *args, **options):
        self.run(**options)

    def run(self, **options):
        self.inner_run(None, **options)

    def inner_run(self, *args, **options):
        # If an exception was silenced in CliParserUtility.exec_from_cli in order
        # to be raised in the child process, raise it now.
        autoreload.raise_last_exception()

        shutdown_message = options.get("shutdown_message", "")
        quit_command = "CTRL-BREAK" if sys.platform == "win32" else "CONTROL-C"

        try:
            handler = self.get_handler(*args, **options)
        except OSError as e:
            # Use helpful error messages instead of ugly tracebacks.
            ERRORS = {
                errno.EACCES: "You don't have permission to access that port.",
                errno.EADDRINUSE: "That port is already in use.",
                errno.EADDRNOTAVAIL: "That IP address can't be assigned to.",
            }
            try:
                error_text = ERRORS[e.errno]
            except KeyError:
                error_text = e
            self.stderr.write("Error: %s" % error_text)
            # Need to use an OS exit because sys.exit doesn't work in a thread
            os._exit(1)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write(shutdown_message)
            sys.exit(0)

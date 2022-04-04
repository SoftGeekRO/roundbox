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

# inspired by Django management commands:
# https://github.com/django/django/blob/main/django/core/management/commands/check.py


from RoundBox.apps import apps
from RoundBox.core import checks
from RoundBox.core.checks.registry import registry
from RoundBox.core.cliparser import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Checks the entire RoundBox project for potential problems."

    requires_system_checks = []

    def add_arguments(self, parser) -> None:
        """

        :param parser:
        :return:
        """
        parser.add_argument("args", metavar="app_label", nargs="*")
        parser.add_argument(
            "--tag",
            "-t",
            action="append",
            dest="tags",
            help="Run only checks labeled with given tag.",
        )
        parser.add_argument(
            "--list-tags",
            action="store_true",
            help="List available tags.",
        )
        parser.add_argument(
            "--deploy",
            action="store_true",
            help="Check deployment settings.",
        )
        parser.add_argument(
            "--fail-level",
            default="ERROR",
            choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
            help=(
                "Message level that will cause the command to exit with a "
                "non-zero status. Default is ERROR."
            ),
        )

    def handle(self, *app_labels, **options) -> None:
        """

        :param app_labels:
        :param options:
        :return:
        """

        include_deployment_checks = options["deploy"]
        if options["list_tags"]:
            self.stdout.write(
                "\n".join(sorted(registry.tags_available(include_deployment_checks)))
            )
            return

        if app_labels:
            app_configs = [apps.get_app_config(app_label) for app_label in app_labels]
        else:
            app_configs = None

        tags = options["tags"]
        if tags:
            try:
                invalid_tag = next(
                    tag
                    for tag in tags
                    if not checks.tag_exists(tag, include_deployment_checks)
                )
            except StopIteration:
                # no invalid tags
                pass
            else:
                raise CommandError(
                    'There is no system check with the "%s" tag.' % invalid_tag
                )

        self.check(
            app_configs=app_configs,
            tags=tags,
            display_num_errors=True,
            include_deployment_checks=include_deployment_checks,
            fail_level=getattr(checks, options["fail_level"]),
        )

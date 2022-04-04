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

from itertools import chain

from RoundBox.utils.inspect import func_accepts_kwargs
from RoundBox.utils.itercompat import is_iterable


class Tags:
    """Built-in tags for internal checks."""

    caches = "caches"  # Checks cache related configuration.
    files = "files"  # Checks file related configuration.
    runtime = "runtime"  # Checks if the project and application meet the minimum requirements
    security = "security"  # Checks security related configuration.
    signals = "signals"  # Checks on signal declarations and handler registrations.


class CheckRegistry:
    """ """

    def __init__(self):
        self.registered_checks = set()
        self.deployment_checks = set()

    def register(self, check=None, *tags, **kwargs):
        """
        Can be used as a function or a decorator. Register given function
        `f` labeled with given `tags`. The function should receive **kwargs
        and return list of Errors and Warnings.
        Example::
            registry = CheckRegistry()
            @registry.register('mytag', 'anothertag')
            def my_check(app_configs, **kwargs):
                # ... perform checks and collect `errors` ...
                return errors
            # or
            registry.register(my_check, 'mytag', 'anothertag')
        """

        def inner(check):
            if not func_accepts_kwargs(check):
                raise TypeError("Check functions must accept keyword arguments (**kwargs).")
            check.tags = tags
            checks = self.deployment_checks if kwargs.get("deploy") else self.registered_checks
            checks.add(check)
            return check

        if callable(check):
            return inner(check)
        else:
            if check:
                tags += (check,)
            return inner

    def run_checks(self, app_configs=None, tags=None, include_deployment_checks=False):
        """Run all registered checks and return list of Errors and Warnings.

        :param app_configs:
        :param tags:
        :param include_deployment_checks:
        :return:
        """

        errors = []
        checks = self.get_checks(include_deployment_checks)

        if tags is not None:
            checks = [check for check in checks if not set(check.tags).isdisjoint(tags)]

        for check in checks:
            new_errors = check(app_configs=app_configs)
            if not is_iterable(new_errors):
                raise TypeError(
                    "The function %r did not return a list. All functions "
                    "registered with the checks registry must return a list." % check,
                )
            errors.extend(new_errors)
        return errors

    def tag_exists(self, tag, include_deployment_checks=False):
        return tag in self.tags_available(include_deployment_checks)

    def tags_available(self, deployment_checks=False):
        return set(chain.from_iterable(check.tags for check in self.get_checks(deployment_checks)))

    def get_checks(self, include_deployment_checks=False):
        checks = list(self.registered_checks)
        if include_deployment_checks:
            checks.extend(self.deployment_checks)
        return checks


registry = CheckRegistry()
register = registry.register
run_checks = registry.run_checks
tag_exists = registry.tag_exists

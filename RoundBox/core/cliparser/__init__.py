#  -*- coding: utf-8 -*-

# This library is heavy inspired by the Django management core module.
# Praise the OpenSource and devs from Django framework and the community
# url: https://github.com/django/django/tree/main/django/core/management

import functools
import os
import pkgutil
import sys
from collections import defaultdict
from difflib import get_close_matches
from importlib import import_module

import RoundBox
from RoundBox.apps import apps
from RoundBox.conf.project_settings import settings
from RoundBox.core.cliparser.base import (
    BaseCommand,
    CommandError,
    CommandParser,
    handle_default_options,
)
from RoundBox.core.cliparser.color import color_style
from RoundBox.core.exceptions import ImproperlyConfigured
from RoundBox.utils import autoreload
from RoundBox.version import __version__


def find_commands(cliparser_dir):
    """
    Given a path to a management directory, return a list of all the command
    names that are available.
    """
    command_dir = os.path.join(cliparser_dir, "commands")
    return [
        name
        for _, name, is_pkg in pkgutil.iter_modules([command_dir])
        if not is_pkg and not name.startswith("_")
    ]


def load_command_class(app_name, name):
    """
    Given a command name and an application name, return the Command
    class instance. Allow all errors raised by the import process
    (ImportError, AttributeError) to propagate.
    """
    module = import_module("%s.cliparser.commands.%s" % (app_name, name))
    return module.Command()


@functools.lru_cache(maxsize=None)
def get_commands():
    """Return the script's main help text, as a string.

        Look for a cliparser.commands package in RoundBox.core, and in each
        installed application -- if a commands package exists, register all
        commands in that package.

        Core commands are always included. If a settings module has been
        specified, also include user-defined commands.

        The dictionary is in the format {command_name: app_name}. Key-value
        pairs from this dictionary can then be used in calls to
        load_command_class(app_name, command_name)

        The dictionary is cached on the first call and reused on subsequent
        calls.

    :return:
    """
    commands = {name: "RoundBox.core" for name in find_commands(__path__[0])}

    if not settings.configured:
        return commands

    for app_config in reversed(apps.get_app_configs()):
        path = os.path.join(app_config.path, "cliparser")
        commands.update({name: app_config.name for name in find_commands(path)})

    return commands


class CliParserUtility:
    """ """

    def __init__(self, argv=None):
        """

        :param argv:
        """

        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        if self.prog_name == "__main__.py":
            self.prog_name = "python3 -m roundbox"
        self.settings_exception = None

    def main_help_text(self, commands_only=False):
        """

        :param commands_only:
        :return:
        """
        if commands_only:
            usage = sorted(get_commands())
        else:
            usage = [
                "",
                "Type '%s help <subcommand>' for help on a specific subcommand."
                % self.prog_name,
                "",
                "Available subcommands:",
            ]
            commands_dict = defaultdict(lambda: [])
            for name, app in get_commands().items():
                if app == "RoundBox.core":
                    app = "RoundBox"
                else:
                    app = app.rpartition(".")[-1]
                commands_dict[app].append(name)
            style = color_style()
            for app in sorted(commands_dict):
                usage.append("")
                usage.append(style.NOTICE("[%s]" % app))
                for name in sorted(commands_dict[app]):
                    usage.append("    %s" % name)
            # Output an extra note if settings are not properly configured
            if self.settings_exception is not None:
                usage.append(
                    style.NOTICE(
                        "Note that only RoundBox core commands are listed "
                        "as settings are not properly configured (error: %s)."
                        % self.settings_exception
                    )
                )

        return "\n".join(usage)

    def fetch_command(self, subcommand):
        """Try to fetch the given subcommand, printing a message with the
        appropriate command called from the command line if it can't be found.

        :param subcommand:
        :return:
        """
        # Get commands outside of try block to prevent swallowing exceptions
        commands = get_commands()
        try:
            app_name = commands[subcommand]
        except KeyError:
            if os.environ.get("ROUNDBOX_SETTINGS_MODULE"):
                # If `subcommand` is missing due to misconfigured settings, the
                # following line will retrigger an ImproperlyConfigured exception
                # (get_commands() swallows the original one) so the user is
                # informed about it.
                settings.INSTALLED_APPS
            elif not settings.configured:
                sys.stderr.write("No RoundBox settings specified.\n")
            possible_matches = get_close_matches(subcommand, commands)
            sys.stderr.write("Unknown command: %r" % subcommand)
            if possible_matches:
                sys.stderr.write(". Did you mean %s?" % possible_matches[0])
            sys.stderr.write("\nType '%s help' for usage.\n" % self.prog_name)
            sys.exit(1)
        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            klass = app_name
        else:
            klass = load_command_class(app_name, subcommand)
        return klass

    def autocomplete(self):
        """Output completion suggestions for BASH.

        The output of this function is passed to BASH's `COMREPLY` variable and
        treated as completion suggestions. `COMREPLY` expects a space
        separated string as the result.

        The `COMP_WORDS` and `COMP_CWORD` BASH environment variables are used
        to get information about the cli input. Please refer to the BASH
        man-page for more information about this variables.

        Subcommand options are saved as pairs. A pair consists of
        the long option string (e.g. '--exclude') and a boolean
        value indicating if the option requires arguments. When printing to
        stdout, an equal sign is appended to options which require arguments.

        Note: If debugging this function, it is recommended to write the debug
        output in a separate file. Otherwise the debug output will be treated
        and formatted as potential completion suggestions.
        """
        # Don't complete if user hasn't sourced bash_completion file.
        if "ROUNDBOX_AUTO_COMPLETE" not in os.environ:
            return

        cwords = os.environ["COMP_WORDS"].split()[1:]
        cword = int(os.environ["COMP_CWORD"])

        try:
            curr = cwords[cword - 1]
        except IndexError:
            curr = ""

        subcommands = [*get_commands(), "help"]
        options = [("--help", False)]

        # subcommand
        if cword == 1:
            print(" ".join(sorted(filter(lambda x: x.startswith(curr), subcommands))))
        # subcommand options
        # special case: the 'help' subcommand has no options
        elif cwords[0] in subcommands and cwords[0] != "help":
            subcommand_cls = self.fetch_command(cwords[0])

            parser = subcommand_cls.create_parser("", cwords[0])
            options.extend(
                (min(s_opt.option_strings), s_opt.nargs != 0)
                for s_opt in parser._actions
                if s_opt.option_strings
            )
            # filter out previously specified options from available options
            prev_opts = {x.split("=")[0] for x in cwords[1 : cword - 1]}
            options = (opt for opt in options if opt[0] not in prev_opts)

            # filter options by current input
            options = sorted((k, v) for k, v in options if k.startswith(curr))
            for opt_label, require_arg in options:
                # append '=' to options which require args
                if require_arg:
                    opt_label += "="
                print(opt_label)
        # Exit code of the bash completion function is never passed back to
        # the user, so it's safe to always exit with 0.
        # For more details see #25420.
        sys.exit(0)

    def exec(self):
        """Given the command-line arguments, figure out which subcommand is being
        run, create a parser appropriate to that command, and run it.

        :return:
        """
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = "help"  # Display help if no arguments were given.

        # Preprocess options to extract --settings and --pythonpath.
        # These options could affect the commands that are available, so they
        # must be processed early.
        parser = CommandParser(
            prog=self.prog_name,
            usage="%(prog)s subcommand [options] [args]",
            add_help=False,
            allow_abbrev=False,
        )
        parser.add_argument("--settings")
        parser.add_argument("--pythonpath")
        parser.add_argument("args", nargs="*")  # catch-all
        try:
            options, args = parser.parse_known_args(self.argv[2:])
            handle_default_options(options)
        except CommandError:
            pass  # Ignore any option errors at this point

        try:
            settings.INSTALLED_APPS
        except ImproperlyConfigured as exc:
            self.settings_exception = exc
        except ImportError as exc:
            self.settings_exception = exc

        # @TODO: check if in the future this section is function for current use
        if settings.configured:
            # Start the auto-reloading dev server even if the code is broken.
            # The hardcoded condition is a code small, but we can't rely on a
            # flag on the command class because we haven't located it yet.
            if subcommand == 'runserver' and "--noreload" not in self.argv:
                try:
                    autoreload.check_errors(RoundBox.setup)()
                except Exception:
                    # The exception will be raised later in the child process
                    # started by the autoreloader. Pretend it didn't happen by
                    # loading an empty list of applications.
                    apps.all_models = defaultdict(dict)
                    apps.app_configs = {}
                    apps.apps_ready = apps.models_ready = apps.ready = True

                    # Remove options not compatible with the built-in runserver
                    # (e.g. options for the contrib.staticfiles' runserver).
                    # Changes here require manually testing as described in
                    # #27522.
                    _parser = self.fetch_command("runserver").create_parser(
                        "RoundBox", "runserver"
                    )
                    _options, _args = _parser.parse_known_args(self.argv[2:])
                    for _arg in _args:
                        self.argv.remove(_arg)
            # In all other cases, django.setup() is required to succeed.
            else:
                RoundBox.setup()

        self.autocomplete()

        if subcommand == "help":
            if "--commands" in args:
                sys.stdout.write(self.main_help_text(commands_only=True) + "\n")
            elif not options.args:
                sys.stdout.write(self.main_help_text() + "\n")
            else:
                self.fetch_command(options.args[0]).print_help(
                    self.prog_name, options.args[0]
                )
        # special case for --version and --help to work, for backwards compatibility
        elif subcommand == "version" or self.argv[1:] == ["--version"]:
            sys.stdout.write(__version__ + "\n")
        elif self.argv[1:] in (["--help"], ["-h"]):
            sys.stdout.write(self.main_help_text() + "\n")
        else:
            self.fetch_command(subcommand).run_from_argv(self.argv)


def exec_from_cli(argv=None):
    """Execute the CliParserUtility

    :param argv:
    :return:
    """

    utility = CliParserUtility(argv)
    return utility.exec()

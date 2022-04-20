#  -*- coding: utf-8 -*-

# Code inspired by: https://github.com/adammck/djappsettings

import importlib
import sys
import traceback
from pathlib import Path

from RoundBox.apps.config import AppConfig
from RoundBox.conf import global_settings
from RoundBox.conf.project_settings import settings
from RoundBox.utils.functional import Settings

# from loguru import logger


class ApplicationConfig:
    """ """

    def __init__(self):
        self._modules = None

        self._strict = getattr(settings, 'SETTINGS_STRICT', True)

    def _import(self, module_name, package=None):
        """

        :param module_name:
        :param package:
        :return:
        """

        try:
            return importlib.import_module(module_name, package)
        except ImportError:
            tb = sys.exc_info()[2]
            traceback_lines = [t for t in traceback.extract_tb(tb) if t[3]]
            if len(traceback_lines) > 2:
                raise

            # the exception was raised from this scope. *module_name*
            # couldn't be imported, which is fine, since allowing that
            # is the purpose of this method.
            return None

    # @TODO: in the future search a solution to make the application configs to be configured locally and selective
    def local_app(self):
        """

        :return:
        """
        app_base_dir = Path(__file__).parent.parent.parts[-1:][0]
        app = AppConfig.create(app_base_dir)

    def _setup(self):
        """

        :return:
        """

        self._modules = []

        for module_name in settings.INSTALLED_APPS:

            settings_module_name = "%s.settings" % module_name
            module = Settings(settings_module_name, False)

            # if not module.mod_loaded:
            #     logger.warning(f"No project {settings_module_name} modules found.\n")
            #     continue

            # check that the app settings module doesn't contain any of
            # the settings already defined by RoundCube in global_settings.
            # Log this potentially ambiguous condition as an ERROR

            for setting_name in dir(module):

                if setting_name != setting_name.upper():
                    continue

                if hasattr(global_settings, setting_name):
                    error_message = f"The '{settings_module_name}' module masks the built-in '{setting_name}' setting."

                    if self._strict:
                        raise AttributeError(error_message)
                    # else:
                    #     logger.warning(error_message)

            # check that none of the settings have already been defined
            # by another app. rather than behave ambiguously (depending
            # on which app was listed first in INSTALLED_APPS), <strike>explode</strike>...
            # Log this potentially ambiguous condition as an ERROR
            for setting_name in dir(module):
                if setting_name != setting_name.upper():
                    continue

                # ignore settings which are defined in the project's
                # settings module, to give project authors a workaround
                # for bad apps which don't PREFIX_ their settings.
                if hasattr(settings, setting_name):
                    continue

                for other_module in self._modules:
                    if hasattr(other_module, setting_name):
                        error_message = f"The '{setting_name}' setting is already defined by the '{other_module}' module."

                        if self._strict:
                            raise AttributeError(error_message)
                        # else:
                        #     logger.warning(error_message)

            # all is well
            self._modules.append(module)

    def __repr__(self):
        if not self._modules:
            return "<ApplicationConfig [Unevaluated]>"
        return f'<ApplicationConfig "{self._modules}">'

    def __getattr__(self, setting_name):
        """

        :param setting_name:
        :return:
        """

        if self._modules is None:
            self._setup()

        # try the project settings first (which also checks the global
        # default settings, which apps are NOT allowed to override).
        if hasattr(settings, setting_name):
            return getattr(self.project_settings, setting_name)

        # then try the app default settings.
        for module in self._modules:
            if hasattr(module, setting_name):
                return getattr(module, setting_name)

        raise AttributeError(f"The {setting_name} setting is not defined.")


app_settings = ApplicationConfig()

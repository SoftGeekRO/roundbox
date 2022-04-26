#  -*- coding: utf-8 -*-

class Apps:
    def __init__(self, installed_apps: dict = ()):
        """ """
        self.apps_ready: bool = None
        self.ready_event = None
        self.app_configs: tuple = None
        self.loading: bool = None
        self._lock: bool = None
        self.ready: bool = None
    def populate(self, installed_apps=None, call_ready=False):
        """Load application configurations.
        Import each application module.
        It is thread-safe and idempotent, but not reentrant.

        # Changes from original:
          - added the call_ready attribute, to switch off/on the calling of ready method

        :param installed_apps:
        :param call_ready:
        :return:
        """
    def get_app_configs(self):
        """

        :return:
        """
    def check_apps_ready(self):
        """

        :return:
        """
    def get_app_config(self, param: str) -> tuple:
        """

        :param param:
        :return:
        """

apps: Apps = Apps

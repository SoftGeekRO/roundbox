#  -*- coding: utf-8 -*-

from argparse import Namespace

class AppConfig:

    name: str = None
    label: str = None

    args_parse: Namespace = None

    def __init__(self, app_name, app_module):
        """

        :param app_name:
        :param app_module:
        """
    def _path_from_module(self, app_module) -> object:
        """Attempt to determine app's filesystem path from its module.
        
        :param app_module: 
        :return: 
        """ ""
    @classmethod
    def create(cls, entry):
        """

        :param entry:
        :return:
        """

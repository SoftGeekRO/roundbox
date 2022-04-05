#  -*- coding: utf-8 -*-

from RoundBox.core.cliparser.signals import post_command, pre_command


def signalcommand(func):
    """Python decorator for management command handle defs that sends out a pre/post signal.

    :param func:
    :return:
    """

    def inner(self, *args, **kwargs):
        pre_command.send(self.__class__, args=args, kwargs=kwargs)
        ret = func(self, *args, **kwargs)
        post_command.send(self.__class__, args=args, kwargs=kwargs, outcome=ret)
        return ret
    return inner

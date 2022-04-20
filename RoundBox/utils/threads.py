#  -*- coding: utf-8 -*-

import multiprocessing

try:
    from setproctitle import setproctitle
except ModuleNotFoundError:
    pass


class ProcessRuntime(multiprocessing.Process):
    def run(self):

        try:
            setproctitle(self._name)
        except NameError as e:
            pass
        if self._target:
            self._target(*self._args, **self._kwargs)

#  -*- coding: utf-8 -*-
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

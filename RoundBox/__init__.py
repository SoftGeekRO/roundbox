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

from RoundBox.const import __version__


def setup():
    """

    :return:
    """

    from RoundBox.apps import apps
    from RoundBox.conf.project_settings import settings
    from RoundBox.utils.log import configure_logging

    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)

    apps.populate(settings.INSTALLED_APPS, call_ready=False)

    # logger.log(f"Start RoundBox framework v{__version__}")
    #
    # if apps.ready:
    #     with Manager() as manager:
    #         queue = manager.Queue()
    #         rlock = manager.RLock()
    #
    #         all_apps = apps.get_app_configs()
    #         jobs = []
    #
    #         for application in all_apps:
    #             p = ProcessRuntime(
    #                 name=application.name, target=application.ready, args=(queue, rlock)
    #             )
    #             jobs.append(p)
    #             p.daemon = True
    #             p.start()
    #
    #         for job in jobs:
    #             job.join()

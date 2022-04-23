#  -*- coding: utf-8 -*-
# A Python "namespace package" http://www.python.org/dev/peps/pep-0382/
# This always goes inside a namespace package's __init__.py

from pkgutil import extend_path

from RoundBox.version import __version__

__path__ = extend_path(__path__, __name__)


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

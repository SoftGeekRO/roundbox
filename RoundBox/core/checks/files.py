#  -*- coding: utf-8 -*-

from pathlib import Path

from RoundBox.conf.project_settings import settings

from . import Error, Tags, register


@register(Tags.files)
def check_setting_file_log_dir(app_configs, **kwargs):
    setting = getattr(settings, "LOG_DIR", None)
    if setting and not Path(setting).is_dir():
        return [
            Error(
                f"The LOG_DIR setting refers to the nonexistent " f"directory '{setting}'.",
                _id="files.E001",
            ),
        ]
    return []

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

from pathlib import Path

from RoundBox.conf.project_settings import settings

from . import Error, Tags, register


@register(Tags.files)
def check_setting_file_log_dir(app_configs, **kwargs):
    setting = getattr(settings, "LOG_DIR", None)
    if setting and not Path(setting).is_dir():
        return [
            Error(
                f"The LOG_DIR setting refers to the nonexistent "
                f"directory '{setting}'.",
                _id="files.E001",
            ),
        ]
    return []

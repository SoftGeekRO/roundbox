⚡ RoundBox
==========

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI](https://img.shields.io/pypi/v/roundbox?label=RoundBox&style=plastic)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/soulraven/roundbox?style=plastic)
[![Build status](https://img.shields.io/github/workflow/status/soulraven/roundbox/merge-to-main?style=plastic)](https://img.shields.io/github/workflow/status/soulraven/roundbox/merge-to-main)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/roundbox?style=plastic)](https://pypi.org/project/roundbox/)
[![License](https://img.shields.io/github/license/soulraven/roundbox?style=plastic)](https://img.shields.io/github/license/soulraven/roundbox)

***

A small lightweight framework for IoT applications, with main goal to not reinvent the wheel every time when a small
project for IoT device is needed.

The framework contains all tools necessary to bootstrap and run a command a single time or using linux crontab.

You can create apps as many as you like and use them for your proper necessity, but consider that each app is liake a
small container with logic.
Each app has the possibility to host specific commands that will be available  when running manage.py.

### 🎈 Special thanks 🎈
To build this framework I have used code inspired by the [Django](https://github.com/django/django) project and also
from [Home Assistant](https://github.com/home-assistant/core) project.

Both projects have a strong code base and lightweight and port on different projects.

***

### 🔧 Installation

The easy way to install RoundBox framework is with [pip]

```bash
$ pip install roundbox
```

If you want to install RoundBox from GitHub use:

```bash
$ pip install git+https://github.com/soulraven/roundbox.git
```

For more detailed install instructions see how [Install] and configure the framework.

***

### ➿ Variables

- set the ROUNDBOX_COLORS environment variable to specify the palette you want to use. For example,
to specify the light palette under a Unix or OS/X BASH shell, you would run the following at a command prompt:

```bash
export ROUNDBOX_COLORS="light"
```

***

### 🖇 Library used

A more detailed list you will find here: [Libraries](https://soulraven.github.io/roundbox/libraries/)

***

### 🌍 Contributions

Contributions of all forms are welcome :)

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## 📝 License

This project is licensed under [GPLv3].

## 👀 Author

Zaharia Constantin, my [GitHub profile] and [GitHub Page]

[GitHub profile]: https://github.com/soulraven/
[Github Page]: https://soulraven.github.io/
[GNU General Public License]: https://www.gnu.org/licenses/quick-guide-gplv3.html
[pip]: https://pip.pypa.io/en/stable/
[GPLv3]: https://soulraven.github.io/roundbox/license
[Install]: https://soulraven.github.io/roundbox/user-guide/topics/install

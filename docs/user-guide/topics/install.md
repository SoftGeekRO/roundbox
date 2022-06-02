# How to install RoundBox

This document will get you up and running with RoundBox.

Install Python
--------------

RoundBox is a Python framework. See [Python docs] for details.

Get the latest version of Python at https://www.python.org/downloads/ or with your operating system's package manager.

Installing an official release with ``pip``
-------------------------------------------

This is the recommended way to install RoundBox.

1. Install [pip]. The easiest is to use the [standalone pip installer]. If your
   distribution already has ``pip`` installed, you might need to update it if
   it's outdated. If it's outdated, you'll know because installation won't
   work.

2. Take a look at [venv]. This tool provides
   isolated Python environments, which are more practical than installing
   packages system-wide. It also allows installing packages without
   administrator privileges.

3. After you've created and activated a virtual environment, enter the command:

```shell
$ python -m pip install roundbox
```

[pip]: https://pip.pypa.io/
[standalone pip installer]: https://pip.pypa.io/en/latest/installation/
[Python docs]: https://docs.python.org/3/
[venv]: https://docs.python.org/3/tutorial/venv.html

Installing the development version
----------------------------------

If you'd like to be able to update your RoundBox code occasionally with the
latest bug fixes and improvements, follow these instructions:

1. Make sure that you have [Git] installed and that you can run its commands
   from a shell. (Enter ``git help`` at a shell prompt to test this.)

2. Check out RoundBox's main development branch like so:

```shell
$ git clone https://github.com/soulraven/roundbox.git
```

This will create a directory ``roundbox`` in your current directory.

1. Make sure that the Python interpreter can load RoundBox's code. The most
   convenient way to do this is to use a virtual environment and [pip].

2. After setting up and activating the virtual environment, run the following
   command:

```shell
$ python -m pip install -e roundbox/
```

This will make RoundBox's code importable, and will also make the
``roundbox-admin`` utility command available. In other words, you're all set!

When you want to update your copy of the RoundBox source code, run the command
``git pull`` from within the ``roundbox`` directory. When you do this, Git will
download any changes.

[Git]: https://git-scm.com/

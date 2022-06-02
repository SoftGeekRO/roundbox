---
tags:
  - settings
  - python
  - module
  - search
---

RoundBox settings
=================

A RoundBox settings file contains all the configuration of your RoundBox installation.
This document explains how settings work and which settings are
available.

## The basics

A settings file is just a Python module with module-level variables.

!!! Note
    If you set `DEBUG` to ``False``, the logging system will not display the debug messages

Because a settings file is a Python module, the following apply:

* It doesn't allow for Python syntax errors.
* It can assign settings dynamically using normal Python syntax.
  For example:

```python
MY_SETTING = [str(i) for i in range(30)]
```

* It can import values from other settings files

## Designating the settings

When you use RoundBox, you have to tell it which settings you're using. Do this by using an environment variable,
`ROUNDBOX_SETTINGS_MODULE`.

The value of `ROUNDBOX_SETTINGS_MODULE` should be in Python path syntax, e.g. ``myproject.settings``.
Note that the settings module should be on the Python [import search path].

[import search path]: https://diveinto.org/python3/your-first-python-program.html#importsearchpath

## Default settings

A RoundBox settings file doesn't have to define any settings if it doesn't need to.
Each setting has a sensible default value. These defaults live in the module `roundbox/conf/global_settings.py`.

Here's the algorithm RoundBox uses in compiling settings:

* Load settings from ``global_settings.py``.
* Load settings from the specified settings file, overriding the global
  settings as necessary.

Note that a settings file should *not* import from ``global_settings``, because
that's redundant.

### Seeing which settings you've changed

The command ``python manage.py diffsettings`` displays differences between the current settings file and RoundBox's
default settings.

## Using settings in Python code

In your RoundBox apps, use settings by importing the object
``roundbox.project_conf.settings``. Example::

```python
from RoundBox.conf.project_settings import settings

    if settings.DEBUG:
        # Do something

```

Note that ``RoundBox.conf.project_settings`` isn't a module -- it's an object. So importing individual settings is not
possible:

```python
from RoundBox.conf.project_settings import DEBUG  # This won't work.

```

Also note that your code should *not* import from either ``global_settings`` or
your own settings file. ``RoundBox.conf.project_settings`` abstracts the concepts of default settings and site-specific
settings; it presents a single interface. It also decouples the code that uses settings from the location of your settings.

## Altering settings at runtime

You shouldn't alter settings in your applications at runtime. For example,
don't do this in a view:

```python
from RoundBox.conf.project_settings import settings

settings.DEBUG = True   # Don't do this!
```

The only place you should assign to settings is in a settings file.

## Security

Because a settings file contains sensitive information, such as the database password, you should make every attempt to
limit access to it. For example, change its file permissions so that only you and your web server's user can read it.
This is especially important in a shared-hosting environment.

## Creating your own settings

There's nothing stopping you from creating your own settings, for your own RoundBox apps, but follow these guidelines:

* Setting names must be all uppercase.
* Don't reinvent an already-existing setting.

For settings that are sequences, RoundBox itself uses lists, but this is only a convention.

## Using settings without setting `ROUNDBOX_SETTINGS_MODULE`

In some cases, you might want to bypass the `ROUNDBOX_SETTINGS_MODULE`
environment variable. For example, if you're using the template system by
itself, you likely don't want to have to set up an environment variable
pointing to a settings module.

> RoundBox.conf.project_settings.configure(default_settings, **settings)

```python
from RoundBox.conf.project_settings import settings

settings.configure(DEBUG=True)
```

Pass ``configure()`` as many keyword arguments as you'd like, with each keyword argument representing a setting and its
value. Each argument name should be all uppercase, with the same name as the settings described above.
If a particular setting is not passed to ``configure()`` and is needed at some later point, RoundBox will use the
default setting value.

Configuring RoundBox in this fashion is mostly necessary -- and, indeed, recommended -- when you're using a piece of
the framework inside a larger application.

Consequently, when configured via ``settings.configure()``, RoundBox will not make any modifications to the process
environment variables (see the documentation of `TIME_ZONE` for why this would normally occur).
It's assumed that you're already in full control of your environment in these cases.

### Custom default settings

If you'd like default values to come from somewhere other than``RoundBox.conf.global_settings``, you can pass in a
module or class that provides the default settings as the ``default_settings``
argument (or as the first positional argument) in the call to ``configure()``.

In this example, default settings are taken from ``myapp_defaults``, and the`DEBUG` setting is set to ``True``,
regardless of its value in ``myapp_defaults``:

```python
from RoundBox.conf.project_settings import settings
from myapp import myapp_defaults

settings.configure(default_settings=myapp_defaults, DEBUG=True)
```

The following example, which uses ``myapp_defaults`` as a positional argument, is equivalent:

```python
settings.configure(myapp_defaults, DEBUG=True)
```

Normally, you will not need to override the defaults in this fashion. The RoundBox defaults are sufficiently tame that
you can safely use them. Be aware that if you do pass in a new default module, it entirely *replaces* the RoundBox
defaults, so you must specify a value for every possible setting that might be used in that code you are importing.
Check in ``RoundBox.conf.global_settings`` for the full list.

### Either ``configure()`` or `ROUNDBOX_SETTINGS_MODULE` is required

If you're not setting the `ROUNDBOX_SETTINGS_MODULE` environment variable, you *must* call ``configure()``
at some point before using any code that reads settings.

If you don't set `ROUNDBOX_SETTINGS_MODULE` and don't call``configure()``, RoundBox will raise an ``ImportError``
exception the first time a setting is accessed.

If you set `ROUNDBOX_SETTINGS_MODULE`, access settings values somehow, *then* call ``configure()``,
RoundBox will raise a ``RuntimeError`` indicating that settings have already been configured.
There is a property for this purpose:

> RoundBox.conf.project_settings.configured

For example::

```python
from RoundBox.conf import settings

if not settings.configured:
    settings.configure(myapp_defaults, DEBUG=True)
```

Also, it's an error to call ``configure()`` more than once, or to call``configure()``after any setting has been accessed.

It boils down to this: Use exactly one of either ``configure()`` or `ROUNDBOX_SETTINGS_MODULE`. Not both, and not neither.

### Calling ``RoundBox.setup()`` is required for "standalone" RoundBox usage

If you're using components of Django "standalone" -- for example, writing a
Python script which loads some Django templates and renders them, or uses the
ORM to fetch some data -- there's one more step you'll need in addition to
configuring settings.

After you've either set `ROUNDBOX_SETTINGS_MODULE` or called ``configure()``, you'll need to call `django.setup()` to load your
settings and populate Django's application registry. For example:

```python
import RoundBox
from RoundBox.conf import project_settings
from myapp import myapp_defaults

project_settings.configure(default_settings=myapp_defaults, DEBUG=True)
RoundBox.setup()

# Now this script or any imported module can use any part of Django it needs.
from myapp import models
```

Note that calling ``RoundBox.setup()`` is only necessary if your code is truly
standalone. When invoked by your web server, or through `roundbox-admin`, RoundBox will handle this for you.

!!! note "``RoundBox.setup()`` may only be called once."
    Therefore, avoid putting reusable application logic in standalone scripts
    so that you have to import from the script elsewhere in your application.
    If you can't avoid that, put the call to ``RoundBox.setup()`` inside an
    ``if`` block::

    ```python
        if __name__ == '__main__':
            import RoundBox
            RoundBox.setup()
    ```

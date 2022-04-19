#  -*- coding: utf-8 -*-

# Levels
DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50


class CheckMessage:
    """ """

    def __init__(self, level, msg: str, hint: str = None, obj=None, _id=None):
        """

        :param level: The severity of the message. Use one of the predefined values: DEBUG, INFO, WARNING, ERROR,
                      CRITICAL. If the level is greater or equal to ERROR, then ROUNDBOX will prevent management
                      commands from executing. Messages with level lower than ERROR (i.e. warnings) are reported to the
                      console, but can be silenced.
        :param msg: A short (less than 80 characters) string describing the problem.
                    The string should not contain newlines.
        :param hint: A single-line string providing a hint for fixing the problem. If no hint can be provided,
                     or the hint is self-evident from the error message, the hint can be omitted, or a value of None
                     can be used.
        :param obj: Optional. An object providing context for the message
                    (for example, the model where the problem was discovered).
                    The object should be a model, field, or manager or any other object that defines a __str__() method.
                    The method is used while reporting all messages and its result precedes the message.
        :param _id: Optional string. A unique identifier for the issue.
                    Identifiers should follow the pattern applabel.X001, where X is one of the letters CEWID,
                    indicating the message severity (C for criticals, E for errors and so).
                    The number can be allocated by the application, but should be unique within that application.
        """
        if not isinstance(level, int):
            raise TypeError("The first argument should be level.")
        self.level = level
        self.msg = msg
        self.hint = hint
        self.obj = obj
        self.id = _id

    def __eq__(self, other):
        return isinstance(other, self.__class__) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in ["level", "msg", "hint", "obj", "id"]
        )

    def __str__(self):

        if self.obj is None:
            obj = "?"
        else:
            obj = str(self.obj)
        _id = "(%s) " % self.id if self.id else ""
        hint = "\n\tHINT: %s" % self.hint if self.hint else ""
        return "%s: %s%s%s" % (obj, _id, self.msg, hint)

    def __repr__(self):
        return "<%s: level=%r, msg=%r, hint=%r, obj=%r, id=%r>" % (
            self.__class__.__name__,
            self.level,
            self.msg,
            self.hint,
            self.obj,
            self.id,
        )

    def is_serious(self, level=ERROR):
        return self.level >= level

    def is_silenced(self):
        from RoundBox.conf.project_settings import settings

        return self.id in settings.SILENCED_SYSTEM_CHECKS


class Debug(CheckMessage):
    """ """

    def __init__(self, *args, **kwargs):
        super().__init__(DEBUG, *args, **kwargs)


class Info(CheckMessage):
    """ """

    def __init__(self, *args, **kwargs):
        super().__init__(INFO, *args, **kwargs)


class Warning(CheckMessage):
    """ """

    def __init__(self, *args, **kwargs):
        super().__init__(WARNING, *args, **kwargs)


class Error(CheckMessage):
    """ """

    def __init__(self, *args, **kwargs):
        super().__init__(ERROR, *args, **kwargs)


class Critical(CheckMessage):
    """ """

    def __init__(self, *args, **kwargs):
        super().__init__(CRITICAL, *args, **kwargs)

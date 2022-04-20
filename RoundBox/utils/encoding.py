#  -*- coding: utf-8 -*-


def punycode(domain):
    """Return the Punycode of the given domain if it's non-ASCII."""
    return domain.encode("idna").decode("ascii")

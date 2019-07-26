"""Descriptive exceptions."""


class DatasetDiscoveryError(Exception):

    """Raised when dataset discovery fails."""


class ContainmentLoopError(Exception):

    """Raised when conflict analysis finds a loop in place containment."""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Descriptive exceptions."""


class DatasetDiscoveryError(Exception):

    """Raised when dataset discovery fails."""


class ContainmentLoopError(Exception):

    """Raised when conflict analysis finds a loop in place containment."""


class JsonConversionError(Exception):

    """Raised when JSON conversion fails."""


class MissingEnvVarError(Exception):
    """Raisded when an expected environment variable is missing."""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

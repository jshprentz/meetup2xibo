"""Application scope holds command line arguments."""


VERSION = "2.1.0"
APP_NAME = "summarize-m2x-logs"


class ApplicationScope:

    """Application scope provides configuration values."""

    def __init__(self, args):
        """Initialize with parsed command line arguments."""
        self._args = args

    @property
    def app_name(self):
        return APP_NAME

    @property
    def debug(self):
        return self._args.debug


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

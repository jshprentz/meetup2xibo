"""Application scope holds command line arguments."""

import meetup2xibo


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
    def email_subject(self):
        """Return the email subject."""
        return self._args.email_subject

    @property
    def email_to(self):
        """Return the email "To" address."""
        return self._args.email_to

    @property
    def infile(self):
        """Return the open input file."""
        return self._args.infile

    @property
    def mappings(self):
        return self._args.mappings

    @property
    def outfile(self):
        """Return the open output file."""
        return self._args.outfile

    @property
    def version(self):
        return meetup2xibo.__version__


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

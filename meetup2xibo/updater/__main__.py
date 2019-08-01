#!/usr/bin/env python

"""Retrieve events from Meetup, extract data to display on signs, and
update the Xibo database."""

from .application_scope import ApplicationScope
from .command_line import parse_args
from .injector import inject_logging_application
import os


def main():
    """Enter the application scope and run the Meetup to Xibo converter with
    logging."""
    scope = ApplicationScope(parse_args(), os.environ)
    inject_logging_application(scope).run()


if __name__ == '__main__':
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

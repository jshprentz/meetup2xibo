#!/usr/bin/env python

"""Summarize meetup2xibo logs."""

from .application_scope import ApplicationScope
from .command_line import parse_args
from .injector import inject_log_summarizer


def main():
    """Enter the application scope and run the Meetup
    to Xibo converter."""
    scope = ApplicationScope(parse_args())
    inject_log_summarizer(scope).run()


if __name__ == '__main__':
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

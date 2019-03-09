"""Command line options."""

import argparse

parser = argparse.ArgumentParser(
        description='Summarize meetup2xibo logs.')

parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Log debug messages (default: info and higher)')


def parse_args(args=None):
    return parser.parse_args(args)


if __name__ == '__main__':

    parse_args(['--help'])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Command line options."""

import argparse

parser = argparse.ArgumentParser(
        description='Download Meetup events into a XIBO CMS')

parser.add_argument(
        '-c', '--conflicts',
        action='store_true',
        help='Log conflict checking event details (default: do not log)')

parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Log debug messages (default: info and higher)')

parser.add_argument(
        '-l', '--logfile',
        default='meetup2xibo.log',
        help='Path to logfile (default: %(default)s)')

parser.add_argument(
        '-m', '--mappings',
        action='store_true',
        help='Log location mappings (default: only with debug messages)')

parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Log to standard error')

parser.add_argument(
        '-w', '--warnings',
        action='store_true',
        help='Log warnings to standard error')


def parse_args(args=None):
    return parser.parse_args(args)


if __name__ == '__main__':

    parse_args(['--help'])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

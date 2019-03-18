"""Command line options."""

import argparse
import sys

parser = argparse.ArgumentParser(
        description='Summarize meetup2xibo logs.')

parser.add_argument(
        'infile',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help="Input file path (default: standard input)")

parser.add_argument(
        'outfile',
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help="Output file path (default: standard output)")

parser.add_argument(
        '-m', '--mappings',
        action='store_true',
        help='Summarize location mappings in CSV format. '
             '(default: summarize logs in HTML format)')

parser.add_argument(
        '-s', '--subject',
        dest='email_subject',
        default="Meetup to Xibo log summary",
        help='Email subject. (default: %(default)s)')

parser.add_argument(
        '-t', '--to',
        dest='email_to',
        default="",
        help='Generate an email message to this address or space '
             'separated addressses. Overrides --mappings option. '
             '(default: no email message)')


def parse_args(args=None):
    return parser.parse_args(args)


if __name__ == '__main__':

    parse_args(['--help'])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

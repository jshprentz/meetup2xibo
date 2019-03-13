"""Command line options."""

import argparse
import sys

parser = argparse.ArgumentParser(
        description='Summarize meetup2xibo logs.')

parser.add_argument(
        'infile',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin)

parser.add_argument(
        'outfile',
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout)

parser.add_argument(
        '-s', '--subject',
        dest='email_subject',
        default=None,
        help='Generate email headers including this Subject.')

parser.add_argument(
        '-t', '--to',
        dest='email_to',
        default=None,
        help='Generate email headers including this To address.')


def parse_args(args=None):
    return parser.parse_args(args)


if __name__ == '__main__':

    parse_args(['--help'])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

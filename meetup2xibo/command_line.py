import argparse

parser = argparse.ArgumentParser(
        description='Download Meetup events into a XIBO database')

parser.add_argument('-l', '--logfile',
        default='meetup2xibo.log',
        help='Path to logfile (default: %(default)s)')

parser.add_argument('-d', '--debug',
        action='store_true',
        help='Log debug messages (default: info and higher)')

parser.add_argument('-v', '--verbose',
        action='store_true',
        help='Log to standard output')

def parse_args(args = None):
    return parser.parse_args(args)


if __name__ == '__main__':

    parse_args(['--help'])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
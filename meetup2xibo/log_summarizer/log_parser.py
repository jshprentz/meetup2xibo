"""Parses logs and collects the interesting information."""

from parsley import makeGrammar, ParseError
from collections import namedtuple


LogLineStart = namedtuple("LogLineStart", "timestamp log_level")
StartLogLine = namedtuple("StartLogLine", "timestamp program")
InsertLogLine = namedtuple("InsertLogLine", "timestamp event")
DeleteLogLine = namedtuple("DeleteLogLine", "timestamp event")
Field = namedtuple("Field", "name value")


GRAMMER = r"""
start_log_line = log_line_start:s 'meetup2xibo' dash 'Start ' rest_of_line:p
        -> StartLogLine(s.timestamp, p)

insert_log_line = log_line_start:s 'XiboEventCrud' dash 'Inserted ' event:e
        -> InsertLogLine(s.timestamp, e)

delete_log_line = log_line_start:s 'XiboEventCrud' dash 'Deleted Xibo' event:e
        -> DeleteLogLine(s.timestamp, e)

other_log_line = log_line_start name dash rest_of_line

log_line_start = timestamp:t dash level:l dash -> LogLineStart(t, l)

timestamp = date:d ' ' time:t -> " ".join((d, t))

date = <digit{4} '-' digit{2} '-' digit{2}>

time = <digit{2} ':' digit{2} ':' digit{2}>:t ',' digit{3} -> t

level = 'INFO' | 'DEBUG' | 'WARNING' | 'ERROR' | 'CRITICAL'

name = <(letterOrDigit | '_')+>

event = 'Event(' fields:f ')' -> f

fields = field:first (', ' field)*:rest -> [first] + rest

field = name:n '=' quoted_value:v -> Field(n, v)

quoted_value = '\'' (~'\'' anything)*:c '\'' -> ''.join(c)

rest_of_line (~'\n' anything)*:c ('\n' | end) -> ''.join(c)

dash = ' - '
"""


def make_log_parser_class():
    """Make a log line parser class."""
    context = {
            'Field': Field,
            'LogLineStart': LogLineStart,
            'StartLogLine': StartLogLine,
            'InsertLogLine': InsertLogLine,
            }
    return makeGrammar(GRAMMER, context)


def parse_error_hash(self):
    """Define missing ParseError.__hash__()."""
    return hash((self.position, self.formatReason()))

ParseError.__hash__ = parse_error_hash

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

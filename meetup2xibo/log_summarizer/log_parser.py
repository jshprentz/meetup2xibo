"""Parses logs and collects the interesting information."""

from parsley import makeGrammar, ParseError
from collections import namedtuple


LogLineStart = namedtuple("LogLineStart", "timestamp log_level")
StartLogLine = namedtuple("StartLogLine", "timestamp program")
InsertLogLine = namedtuple("InsertLogLine", "timestamp event")
DeleteLogLine = namedtuple("DeleteLogLine", "timestamp event")
UpdateLogLine = namedtuple("UpdateLogLine", "timestamp before after")
UpdateFromLogLine = namedtuple("UpdateFromLogLine", "timestamp event")
UpdateToLogLine = namedtuple("UpdateToLogLine", "timestamp event")
Field = namedtuple("Field", "name value")


GRAMMER = r"""
log_lines = (log_line)*:l

log_line = (start_log_line | insert_log_line | delete_log_line | update_log_line | other_log_line) '\n'

start_log_line :counter = log_line_start('meetup2xibo'):s 'Start ' rest_of_line:p
        -> counter.count(p)

insert_log_line = log_line_start('XiboEventCrud'):s 'Inserted ' event:e
        -> InsertLogLine(s.timestamp, e)

delete_log_line = log_line_start('XiboEventCrud'):s 'Deleted Xibo' event:e
        -> DeleteLogLine(s.timestamp, e)

update_log_line = update_from_log_line:f '\n' update_to_log_line:t
        -> UpdateLogLine(f.timestamp, f.event, t.event)

update_from_log_line = log_line_start('XiboEventCrud'):s 'Updated from Xibo' event:e
        -> UpdateFromLogLine(s.timestamp, e)

update_to_log_line = log_line_start('XiboEventCrud'):s 'Updated to ' event:e
        -> UpdateToLogLine(s.timestamp, e)

other_log_line = log_line_start name dash rest_of_line

log_line_start :name = timestamp:t dash level:l dash name dash -> LogLineStart(t, l)

timestamp = date:d ' ' time:t -> " ".join((d, t))

date = <digit{4} '-' digit{2} '-' digit{2}>

time = <digit{2} ':' digit{2} ':' digit{2}>:t ',' digit{3} -> t

level = 'INFO' | 'DEBUG' | 'WARNING' | 'ERROR' | 'CRITICAL'

name = <(letterOrDigit | '_')+>

event = 'Event(' fields:f ')' -> f

fields = field:first (', ' field)*:rest -> [first] + rest

field = name:n '=' quoted_value:v -> Field(n, v)

quoted_value = ( '\'' | '"' ):q (escaped_char | ~exactly(q) anything)*:c exactly(q) -> ''.join(c)

escaped_char = '\\' ( '\\' | '\'' | '"' )

rest_of_line (~'\n' anything)*:c -> ''.join(c)

end_of_line ('\n' | end)

dash = ' - '
"""


def make_log_parser_class():
    """Make a log line parser class."""
    context = {
            'Field': Field,
            'LogLineStart': LogLineStart,
            'StartLogLine': StartLogLine,
            'InsertLogLine': InsertLogLine,
            'DeleteLogLine': DeleteLogLine,
            'UpdateLogLine': UpdateLogLine,
            'UpdateFromLogLine': UpdateFromLogLine,
            'UpdateToLogLine': UpdateToLogLine,
            }
    return makeGrammar(GRAMMER, context)


def parse_error_hash(self):
    """Define missing ParseError.__hash__()."""
    return hash((self.position, self.formatReason()))

ParseError.__hash__ = parse_error_hash

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

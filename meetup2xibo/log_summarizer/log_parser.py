"""Parses logs and collects the interesting information."""

from .event import Event
from .log_lines import InsertEventLogLine, DeleteEventLogLine, \
    UpdateEventLogLine, UnknownLocationLogLine, EventLocationLogLine, \
    SpecialLocationLogLine, RetireEventLogLine
from parsley import makeGrammar, ParseError
from collections import namedtuple


LogLineStart = namedtuple("LogLineStart", "timestamp log_level")
UpdateToLogLine = namedtuple("UpdateToLogLine", "timestamp event")
Field = namedtuple("Field", "name value")
Summary = namedtuple("Summary", "counter crud_lister location_mapper")
SpecialLocation = namedtuple(
        "SpecialLocation",
        "meetup_id location override comment")


GRAMMER = r"""
log_lines :summary = log_line(summary)*

log_line :summary = (start_log_line(summary.counter)
        | event_log_line(summary.crud_lister)
        | event_location_log_line:l
                -> summary.location_mapper.add_event_location_log_line(l)
        | other_log_line) '\n'

start_log_line :counter = log_line_start('meetup2xibo'):s
        'Start ' rest_of_line:p
        -> counter.count(p)

event_log_line :crud_lister = (insert_log_line
        | delete_log_line
        | retire_log_line
        | update_log_line
        | unknown_location_log_line
        | special_location_log_line):log_line
        -> crud_lister.add_log_line(log_line)

insert_log_line = log_line_start('XiboEventCrud'):s 'Inserted ' event:e
        -> InsertEventLogLine(s.timestamp, e)

delete_log_line = log_line_start('XiboEventCrud'):s 'Deleted Xibo' event:e
        -> DeleteEventLogLine(s.timestamp, e)

retire_log_line = log_line_start('XiboEventCrud'):s 'Retired Xibo' event:e
        -> RetireEventLogLine(s.timestamp, e)

update_log_line = update_from_log_line:f '\n' update_to_log_line:t
        -> UpdateEventLogLine(t.timestamp, f, t.event)

update_from_log_line = log_line_start('XiboEventCrud')
        'Updated from Xibo' event:e
        -> e

update_to_log_line = log_line_start('XiboEventCrud'):s
        'Updated to ' event:e
        -> UpdateToLogLine(s.timestamp, e)

unknown_location_log_line = log_line_start('LocationChooser'):s
        'Unknown location for Partial' event:e
        -> UnknownLocationLogLine(s.timestamp, e)

special_location_log_line = log_line_start('SpecialEventsMonitor'):s
        'No longer needed ' special_location:l
        -> SpecialLocationLogLine(s.timestamp, l)

event_location_log_line = log_line_start('EventConverter'):s
        'Location=' quoted_value:l ' MeetupEvent=Partial' event:e
        -> EventLocationLogLine(s.timestamp, l, e)

special_location = 'SpecialLocation(' fields:f ')'
        -> SpecialLocation(**dict(f))

other_log_line = rest_of_line

log_line_start :name = timestamp:t dash level:l dash name dash
        -> LogLineStart(t, l)

timestamp = date:d ' ' time:t -> " ".join((d, t))

event_timestamp = date:d ' ' event_time:t -> " ".join((d, t))

date = <digit{4} '-' digit{2} '-' digit{2}>

time = <digit{2} ':' digit{2}>:t ':' digit{2} ',' digit{3} -> t

event_time = <digit{2} ':' digit{2}>:t ':' digit{2} -> t

level = 'INFO' | 'DEBUG' | 'WARNING' | 'ERROR' | 'CRITICAL'

name = <(letterOrDigit | '_')+>


event = 'Event(' fields:f ')' -> Event.from_fields(f)

fields = field:first (', ' field)*:rest -> [first] + rest

field = time_field | boolean_field | other_field

time_field = time_field_name:n '=\'' event_timestamp:v '\'' -> Field(n, v)

time_field_name = 'start_time' | 'end_time'

boolean_field = boolean_field_name:n '=' boolean_value:v -> Field(n, v)

boolean_value = 'True' -> True
        | 'False' -> False

boolean_field_name = 'override'

other_field = name:n '=' quoted_value:v -> Field(n, v)

quoted_value = ( '\'' | '"' ):q
        (escaped_char | ~exactly(q) anything)*:c
        exactly(q)
        -> ''.join(c)

escaped_char = '\\' ( '\\' | '\'' | '"' )

rest_of_line <(~'\n' anything)*>

end_of_line ('\n' | end)

dash = ' - '
"""


def make_log_parser_class():
    """Make a log line parser class."""
    context = {
            'Field': Field,
            'Event': Event,
            'InsertEventLogLine': InsertEventLogLine,
            'DeleteEventLogLine': DeleteEventLogLine,
            'RetireEventLogLine': RetireEventLogLine,
            'UpdateEventLogLine': UpdateEventLogLine,
            'UnknownLocationLogLine': UnknownLocationLogLine,
            'SpecialLocation': SpecialLocation,
            'SpecialLocationLogLine': SpecialLocationLogLine,
            'EventLocationLogLine': EventLocationLogLine,
            'LogLineStart': LogLineStart,
            'UpdateToLogLine': UpdateToLogLine,
            }
    return makeGrammar(GRAMMER, context)


def parse_error_hash(self):
    """Define missing ParseError.__hash__()."""
    return hash((self.position, self.formatReason()))


ParseError.__hash__ = parse_error_hash

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

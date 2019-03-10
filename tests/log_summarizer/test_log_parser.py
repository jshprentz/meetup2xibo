"""Test log parser productions."""

from ..context import meetup2xibo
from meetup2xibo.log_summarizer.log_parser import make_log_parser_class
from parsley import ParseError
import pytest

def parse_error_hash(self):
    """Define missing ParseError.__hash__()."""
    return hash((self.position, self.formatReason()))

ParseError.__hash__ = parse_error_hash


@pytest.fixture(scope="module")
def log_parser_class():
    """Return a log parser class, which creates a parser when called
    with string."""
    return make_log_parser_class()

def test_dash(log_parser_class):
    """Test recognizing the dash separator between log line components."""
    parser = log_parser_class(" - ")
    assert parser.dash() == " - "

def test_date(log_parser_class):
    """Test recognizing a date."""
    parser = log_parser_class("2019-03-08")
    assert parser.date() == "2019-03-08"

def test_time(log_parser_class):
    """Test recognizing a time."""
    parser = log_parser_class("06:14:59,274")
    assert parser.time() == "06:14:59"

def test_date_time(log_parser_class):
    """Test recognizing a timestamp."""
    parser = log_parser_class("2019-02-18 16:34:52,274")
    assert parser.timestamp() == "2019-02-18 16:34:52"

def test_level_info(log_parser_class):
    """Test recognizing the info logging level."""
    parser = log_parser_class("INFO")
    assert parser.level() == "INFO"

def test_level_warning(log_parser_class):
    """Test recognizing the warning logging level."""
    parser = log_parser_class("WARNING")
    assert parser.level() == "WARNING"

def test_name(log_parser_class):
    """Test recognizing a name."""
    parser = log_parser_class("AntiFlapper_")
    assert parser.name() == "AntiFlapper_"

def test_rest_of_line(log_parser_class):
    """Test recognizing the rest of a line."""
    parser = log_parser_class("The quick brown fox\n")
    assert parser.rest_of_line() == "The quick brown fox"

def test_log_line_start(log_parser_class):
    """Test recognizing the start of a line."""
    parser = log_parser_class("2019-03-04 16:52:14,131 - INFO - ")
    assert parser.log_line_start() == ("2019-03-04 16:52:14", "INFO")

def test_start_log_line(log_parser_class, sample_log_lines):
    """Test recognizing a start log line."""
    log_line = sample_log_lines.start_line()
    parser = log_parser_class(log_line)
    assert parser.start_log_line() == ("2019-03-04 06:00:53", "meetup2xibo 2.0.1")

def test_quoted_value(log_parser_class):
    """Test recognizing a quoted value."""
    parser = log_parser_class("'The quick brown fox'")
    assert parser.quoted_value() == "The quick brown fox"

def test_field(log_parser_class):
    """Test recognizing a field."""
    parser = log_parser_class("foo='bar'")
    assert parser.field() == ("foo", "bar")

def test_fields_1(log_parser_class):
    """Test recognizing fields with one field."""
    parser = log_parser_class("foo='bar'")
    assert parser.fields() == [("foo", "bar")]

def test_fields_2(log_parser_class):
    """Test recognizing fields with two fields."""
    parser = log_parser_class("foo='bar', id='123'")
    assert parser.fields() == [("foo", "bar"), ("id", "123")]

def test_event(log_parser_class):
    """Test recognizing an event."""
    parser = log_parser_class(
            "Event(xibo_id='430', meetup_id='zvbxrpl2', "
            "name='Nova Labs Open House', location='Orange Bay', "
            "start_time='2019-02-26 15:00:00', end_time='2019-02-26 17:00:00')")
    assert parser.event() == [
            ('xibo_id', '430'),
            ('meetup_id', 'zvbxrpl2'),
            ('name', 'Nova Labs Open House'),
            ('location', 'Orange Bay'),
            ('start_time', '2019-02-26 15:00:00'),
            ('end_time', '2019-02-26 17:00:00')]

def test_insert_log_line(log_parser_class, sample_log_lines):
    """Test recognizing an insert log line."""
    log_line = sample_log_lines.insert_line()
    parser = log_parser_class(log_line)
    assert parser.insert_log_line() == ('2019-03-04 06:00:12', [
            ('meetup_id', 'tmnbrqyzhbhb'),
            ('name', 'Maker Faire Organizing Team'),
            ('location', 'Classroom A'),
            ('start_time', '2019-05-05 18:00:00'),
            ('end_time', '2019-05-05 20:00:00'),
            ])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

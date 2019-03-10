"""Test log parser productions."""

from ..context import meetup2xibo
from meetup2xibo.log_summarizer.log_parser import make_log_parser_class, Field
from meetup2xibo.log_summarizer.start_counter import StartCounter
from parsley import ParseError
import pytest

#def parse_error_hash(self):
#    """Define missing ParseError.__hash__()."""
#    return hash((self.position, self.formatReason()))

#ParseError.__hash__ = parse_error_hash


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
    parser = log_parser_class("The quick brown fox")
    assert parser.rest_of_line() == "The quick brown fox"

def test_log_line_start(log_parser_class):
    """Test recognizing the start of a line."""
    parser = log_parser_class("2019-03-04 16:52:14,131 - INFO - foo - ")
    assert parser.log_line_start("foo") == ("2019-03-04 16:52:14", "INFO")

def test_start_log_line(log_parser_class, sample_log_lines):
    """Test recognizing a start log line."""
    counter = StartCounter()
    log_line = sample_log_lines.start_line()
    parser = log_parser_class(log_line)
    parser.start_log_line(counter)
    assert counter.counts() == [("meetup2xibo 2.0.1", 1)]

def test_quoted_value(log_parser_class):
    """Test recognizing a quoted value."""
    parser = log_parser_class("'The quick brown fox'")
    assert parser.quoted_value() == "The quick brown fox"

def test_field(log_parser_class):
    """Test recognizing a field."""
    parser = log_parser_class("foo='bar'")
    assert parser.field() == ("foo", "bar")

def test_field_with_single_quote(log_parser_class):
    """Test recognizing a field containing a single quote."""
    parser = log_parser_class('''name="Test single quote ' here"''')
    assert parser.field() == ("name", "Test single quote ' here")

def test_field_with_double_quote(log_parser_class):
    """Test recognizing a field containing a double quote."""
    parser = log_parser_class("""name='Test double quote " here'""")
    assert parser.field() == ("name", 'Test double quote " here')

def test_field_with_single_and_double_quote(log_parser_class):
    """Test recognizing a field containing both a single quote and a double
    quote."""
    parser = log_parser_class(r"""name='Test single quote \' and double quote " together'""")
    assert parser.field() == ("name", 'Test single quote \' and double quote " together')

def test_field_with_backslash(log_parser_class):
    """Test recognizing a field containing a backslash."""
    parser = log_parser_class(r"""name='Test backslash \\ here'""")
    assert parser.field() == ("name", 'Test backslash \\ here')

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
    assert parser.insert_log_line() == ('2019-03-04 06:00:12', sample_log_lines.insert_fields)

def test_delete_log_line(log_parser_class, sample_log_lines):
    """Test recognizing a delete log line."""
    log_line = sample_log_lines.delete_line()
    parser = log_parser_class(log_line)
    assert parser.delete_log_line() == ('2019-03-04 06:00:57', sample_log_lines.delete_fields)

def test_update_log_line(log_parser_class, sample_log_lines):
    """Test recognizing a pair of update log lines."""
    log_line = sample_log_lines.update_line()
    parser = log_parser_class(log_line)
    timestamp, before, after =  parser.update_log_line()
    assert timestamp == '2019-03-04 06:00:59'
    assert before == sample_log_lines.update_before_fields
    assert after == sample_log_lines.update_after_fields


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

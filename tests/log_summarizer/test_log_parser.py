"""Test log parser productions."""

from meetup2xibo.log_summarizer.log_parser import make_log_parser_class, Field, Summary
from meetup2xibo.log_summarizer.event import Event
from meetup2xibo.log_summarizer.log_lines import InsertEventLogLine, \
    UpdateEventLogLine, DeleteEventLogLine, RetireEventLogLine, \
    UnknownLocationLogLine, EventLocationLogLine, SpecialLocationLogLine
from meetup2xibo.log_summarizer.start_counter import StartCounter
from meetup2xibo.log_summarizer.crud_lister import CrudLister
from meetup2xibo.log_summarizer.location_mapper import LocationMapper
from parsley import ParseError
import pytest


@pytest.fixture(scope="module")
def log_parser_class():
    """Return a log parser class, which creates a parser when called
    with string."""
    return make_log_parser_class()

@pytest.fixture
def crud_lister():
    """Return a CRUD lister."""
    return CrudLister()

@pytest.fixture
def counter():
    """Return a start counter."""
    return StartCounter()

@pytest.fixture
def location_mapper():
    """Return a location mapper."""
    return LocationMapper()

@pytest.fixture
def summary(counter, crud_lister, location_mapper):
    """Return a summary tuple."""
    return Summary(counter, crud_lister, location_mapper)

def test_dash(log_parser_class):
    """Test recognizing the dash separator between log line components."""
    parser = log_parser_class(" - ")
    assert parser.dash() == " - "

def test_date(log_parser_class):
    """Test recognizing a date."""
    parser = log_parser_class("2019-03-08")
    assert parser.date() == "2019-03-08"

def test_time(log_parser_class):
    """Test recognizing a time, keeping only hh:mm."""
    parser = log_parser_class("06:14:59,274")
    assert parser.time() == "06:14"

def test_date_time(log_parser_class):
    """Test recognizing a timestamp."""
    parser = log_parser_class("2019-02-18 16:34:52,274")
    assert parser.timestamp() == "2019-02-18 16:34"

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
    assert parser.log_line_start("foo") == ("2019-03-04 16:52", "INFO")

def test_start_log_line(log_parser_class, sample_log_lines, counter):
    """Test recognizing a start log line."""
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

def test_field_with_start_time(log_parser_class):
    """Test recognizing a field containing a start time, which should suppress
    seconds."""
    parser = log_parser_class("start_time='2019-02-24 11:22:33'")
    assert parser.field() == ("start_time", "2019-02-24 11:22")

def test_field_with_end_time(log_parser_class):
    """Test recognizing a field containing a end time, which should suppress
    seconds."""
    parser = log_parser_class("end_time='2019-02-24 11:22:33'")
    assert parser.field() == ("end_time", "2019-02-24 11:22")

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
    expected_event = Event(
            xibo_id='430',
            meetup_id='zvbxrpl2',
            name='Nova Labs Open House',
            location='Orange Bay',
            start_time='2019-02-26 15:00',
            end_time='2019-02-26 17:00')
    assert parser.event() == expected_event

def test_insert_log_line(log_parser_class, sample_log_lines):
    """Test recognizing an insert log line."""
    log_line_text = sample_log_lines.insert_line()
    parser = log_parser_class(log_line_text)
    log_line = parser.insert_log_line()
    assert isinstance(log_line, InsertEventLogLine)
    assert log_line.timestamp == '2019-03-04 06:00'
    assert log_line.meetup_id == 'tmnbrqyzhbhb'

def test_delete_log_line(log_parser_class, sample_log_lines):
    """Test recognizing a delete log line."""
    log_line_text = sample_log_lines.delete_line()
    parser = log_parser_class(log_line_text)
    log_line = parser.delete_log_line()
    assert isinstance(log_line, DeleteEventLogLine)
    assert log_line.timestamp == '2019-03-04 06:00'
    assert log_line.meetup_id == '258645498'

def test_retire_log_line(log_parser_class, sample_log_lines):
    """Test recognizing a retire log line."""
    log_line_text = sample_log_lines.retire_line()
    parser = log_parser_class(log_line_text)
    log_line = parser.retire_log_line()
    assert isinstance(log_line, RetireEventLogLine)
    assert log_line.timestamp == '2019-03-04 06:00'
    assert log_line.meetup_id == '257907613'

def test_update_log_line(log_parser_class, sample_log_lines):
    """Test recognizing a pair of update log lines."""
    log_line_text = sample_log_lines.update_line()
    parser = log_parser_class(log_line_text)
    log_line = parser.update_log_line()
    assert isinstance(log_line, UpdateEventLogLine)
    assert log_line.timestamp == '2019-03-04 06:00'
    assert log_line.meetup_id == '259565142'

def test_unknown_location_log_line(log_parser_class, sample_log_lines):
    """Test recognizing an unknown location log line."""
    log_line_text = sample_log_lines.unknown_location_line()
    parser = log_parser_class(log_line_text)
    log_line = parser.unknown_location_log_line()
    assert isinstance(log_line, UnknownLocationLogLine)
    assert log_line.timestamp == '2019-03-04 06:00'
    assert log_line.meetup_id == '259565055'

def test_special_location_log_line(log_parser_class, sample_log_lines):
    """Test recognizing a special location log line."""
    log_line_text = sample_log_lines.special_location_line()
    parser = log_parser_class(log_line_text)
    log_line = parser.special_location_log_line()
    assert isinstance(log_line, SpecialLocationLogLine)
    assert log_line.timestamp == '2019-03-04 06:00'
    assert log_line.meetup_id == '258645498'
    assert log_line.special_location.override is False

def test_event_location_log_line(log_parser_class, sample_log_lines):
    """Test recognizing an event location log line."""
    log_line_text = sample_log_lines.event_location_line()
    parser = log_parser_class(log_line_text)
    log_line = parser.event_location_log_line()
    assert isinstance(log_line, EventLocationLogLine)
    assert log_line.timestamp == '2019-03-04 06:00'
    assert log_line.meetup_id == '259405866'
    assert log_line.location == 'Woodshop'

def test_event_log_line(log_parser_class, sample_log_lines, crud_lister):
    """Test recognizing an event log line."""
    log_line_text = sample_log_lines.insert_line()
    parser = log_parser_class(log_line_text)
    parser.event_log_line(crud_lister)
    meetup_id = 'tmnbrqyzhbhb'
    log_line = crud_lister.event_logs[meetup_id].log_lines[0]
    assert isinstance(log_line, InsertEventLogLine)
    assert log_line.timestamp == '2019-03-04 06:00'
    assert log_line.meetup_id == meetup_id

def test_log_line_insert(log_parser_class, sample_log_lines, crud_lister, counter, summary):
    """Test recognizing a log line that is an insert line."""
    log_line_text = sample_log_lines.insert_line() + "\n"
    parser = log_parser_class(log_line_text)
    parser.log_line(summary)
    meetup_id = 'tmnbrqyzhbhb'
    log_line = crud_lister.event_logs[meetup_id].log_lines[0]
    assert isinstance(log_line, InsertEventLogLine)
    assert log_line.timestamp == '2019-03-04 06:00'
    assert log_line.meetup_id == 'tmnbrqyzhbhb'
    assert counter.counts() == []

def test_log_line_start(log_parser_class, sample_log_lines, crud_lister,
        counter, location_mapper, summary):
    """Test recognizing a log line that is a start line."""
    log_line_text = sample_log_lines.start_line() + "\n"
    parser = log_parser_class(log_line_text)
    parser.log_line(summary)
    assert counter.counts() == [("meetup2xibo 2.0.1", 1)]
    assert crud_lister.event_logs == {}
    assert not location_mapper.has_mappings()

def test_log_line_event_location(log_parser_class, sample_log_lines,
        crud_lister, counter, location_mapper, summary):
    """Test recognizing a log line that is an event location mapping."""
    log_line_text = sample_log_lines.event_location_line() + "\n"
    parser = log_parser_class(log_line_text)
    parser.log_line(summary)
    assert counter.counts() == []
    assert crud_lister.event_logs == {}
    assert location_mapper.mapping_list()[0].location == "Woodshop"

def test_log_line_other(log_parser_class, sample_log_lines, crud_lister, counter, summary):
    """Test recognizing a log line that is an unrecognized line."""
    log_line_text = "Something else\n"
    parser = log_parser_class(log_line_text)
    parser.log_line(summary)
    assert counter.counts() == []
    assert crud_lister.event_logs == {}

def test_log_lines(log_parser_class, sample_log_lines, crud_lister, counter,
        location_mapper, summary):
    """Test recognizing a log lines."""
    log_line_text = "\n".join([
            sample_log_lines.start_line(),
            sample_log_lines.insert_line(),
            sample_log_lines.event_location_line(),
            "Something else\n"])
    parser = log_parser_class(log_line_text)
    parser.log_lines(summary)
    meetup_id = 'tmnbrqyzhbhb'
    log_line = crud_lister.event_logs[meetup_id].log_lines[0]
    assert isinstance(log_line, InsertEventLogLine)
    assert log_line.timestamp == '2019-03-04 06:01'
    assert log_line.meetup_id == meetup_id
    assert counter.counts() == [("meetup2xibo 2.0.1", 1)]
    assert location_mapper.mapping_list()[0].location == "Woodshop"

def test_log_lines_with_special_location(log_parser_class, sample_log_lines,
        crud_lister, summary):
    """Test recognizing a log lines with a special location."""
    delete_line_text = sample_log_lines.delete_line()
    special_location_line_text =sample_log_lines.special_location_line()
    log_line_text = "\n".join([
            delete_line_text,
            special_location_line_text,
            "Something else\n"])
    parser = log_parser_class(log_line_text)
    parser.log_lines(summary)
    meetup_id = '258645498'
    event_crud = crud_lister.event_logs[meetup_id]
    log_line_0 = event_crud.log_lines[0]
    assert isinstance(log_line_0, DeleteEventLogLine)
    assert log_line_0.timestamp == '2019-03-04 06:00'
    assert log_line_0.meetup_id == meetup_id
    assert event_crud.final_event == log_line_0.final_event
    log_line_1 = event_crud.log_lines[1]
    assert isinstance(log_line_1, SpecialLocationLogLine)
    assert log_line_1.timestamp == '2019-03-04 06:01'
    assert log_line_1.meetup_id == meetup_id


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Test log lines."""

from ..context import meetup2xibo
from meetup2xibo.log_summarizer.log_lines import InsertEventLogLine, UpdateEventLogLine, DeleteEventLogLine
from meetup2xibo.log_summarizer.event import Event
import pytest

SAMPLE_MEETUP_ID = 'qlpqsqyzhbqb'
SAMPLE_NAME = 'Arduino User Group'
SAMPLE_LOCATION = 'Conference Room 3'
SAMPLE_START_TIME = '2019-05-12 15:00:00'
SAMPLE_END_TIME = '2019-05-12 17:00:00'

SAMPLE_LOG_TIME = '2019-03-08 09:12:34'

#@pytest.fixture
#def crud_lister():
#    """Return an event CRUD log line lister."""
#    return CrudLister()

def make_event(
        name=SAMPLE_NAME,
        location=SAMPLE_LOCATION,
        start_time=SAMPLE_START_TIME,
        end_time=SAMPLE_END_TIME,
        meetup_id=SAMPLE_MEETUP_ID,
        xibo_id=None):
    """Make an event with default sample values."""
    return Event(name, location, start_time, end_time, meetup_id, xibo_id)

@pytest.fixture
def event():
    """Return an event with the sample field values."""
    return make_event()

def test_meetup_id_in_insert_event_log_line(event):
    """Test getting the Meetup ID from an insert event log line."""
    log_line = InsertEventLogLine(SAMPLE_LOG_TIME, event)
    assert log_line.meetup_id == SAMPLE_MEETUP_ID

def test_meetup_id_in_delete_event_log_line(event):
    """Test getting the Meetup ID from an delete event log line."""
    log_line = DeleteEventLogLine(SAMPLE_LOG_TIME, event)
    assert log_line.meetup_id == SAMPLE_MEETUP_ID

def test_meetup_id_in_update_event_log_line(event):
    """Test getting the Meetup ID from an update event log line."""
    after_event = make_event(location="Somewhere else")
    log_line = UpdateEventLogLine(SAMPLE_LOG_TIME, event, after_event)
    assert log_line.meetup_id == SAMPLE_MEETUP_ID

def test_before_event_in_update_event_log_line(event):
    """Test getting the before event from an update event log line."""
    after_event = make_event(location="Somewhere else")
    log_line = UpdateEventLogLine(SAMPLE_LOG_TIME, event, after_event)
    assert log_line.before_event == event

def test_after_event_in_update_event_log_line(event):
    """Test getting the after event from an update event log line."""
    after_event = make_event(location="Somewhere else")
    log_line = UpdateEventLogLine(SAMPLE_LOG_TIME, event, after_event)
    assert log_line.after_event == after_event



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

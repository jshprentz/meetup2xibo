"""Test event log line collection and reporting."""

from ..context import meetup2xibo
from meetup2xibo.log_summarizer.event_log import EventLog
import pytest


@pytest.fixture
def event_log():
    """Return an event log line lister."""
    return EventLog()

def test_add_log_line(event_log, sample_log_lines):
    """Test adding a log line."""
    log_line = sample_log_lines.make_insert_log_line()
    event_log.add_log_line(log_line)
    assert event_log.log_lines == [log_line]

def test_add_unknown_locaation_log_line(event_log, sample_log_lines):
    """Test adding an unknown location log line."""
    log_line = sample_log_lines.make_unknown_location_log_line()
    event_log.add_unknown_location_log_line(log_line)
    assert event_log.log_lines == [log_line]

def test_add_unknown_locaation_log_line_repeated(event_log, sample_log_lines):
    """Test adding a repeated unknown location log line."""
    log_line_1 = sample_log_lines.make_unknown_location_log_line()
    log_line_2 = sample_log_lines.make_unknown_location_log_line()
    event_log.add_unknown_location_log_line(log_line_1)
    event_log.add_unknown_location_log_line(log_line_2)
    assert event_log.log_lines == [log_line_1]

def test_final_event(event_log, sample_log_lines):
    """Test getting the final log line."""
    insert_log_line = sample_log_lines.make_insert_log_line()
    update_log_line = sample_log_lines.make_update_log_line()
    event_log.add_log_line(insert_log_line)
    event_log.add_log_line(update_log_line)
    assert event_log.final_event == update_log_line.after_event





# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

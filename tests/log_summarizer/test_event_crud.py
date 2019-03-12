"""Test event CRUD collection and reporting."""

from ..context import meetup2xibo
from meetup2xibo.log_summarizer.event_crud import EventCrud
import pytest


@pytest.fixture
def event_crud():
    """Return an event CRUD log line lister."""
    return EventCrud()

def test_add_log_line(event_crud, sample_log_lines):
    """Test adding a log line."""
    log_line = sample_log_lines.make_insert_log_line()
    event_crud.add_log_line(log_line)
    assert event_crud.log_lines == [log_line]

def test_final_event(event_crud, sample_log_lines):
    """Test getting the final log line."""
    insert_log_line = sample_log_lines.make_insert_log_line()
    update_log_line = sample_log_lines.make_update_log_line()
    event_crud.add_log_line(insert_log_line)
    event_crud.add_log_line(update_log_line)
    assert event_crud.final_event == update_log_line.after_event





# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

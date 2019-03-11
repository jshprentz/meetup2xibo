"""Test the event CRUD log line lister."""

from ..context import meetup2xibo
from meetup2xibo.log_summarizer.crud_lister import CrudLister
import pytest


@pytest.fixture
def crud_lister():
    """Return an event CRUD log line lister."""
    return CrudLister()

def test_add_insert_event(crud_lister, sample_log_lines):
    """Test adding an insert event log line to the lister."""
    log_line = sample_log_lines.make_insert_log_line()
    meetup_id = log_line.meetup_id
    crud_lister.add_log_line(log_line)
    assert crud_lister.event_cruds[meetup_id].log_lines == [log_line]




# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

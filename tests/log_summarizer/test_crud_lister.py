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

def test_sorted_event_cruds(crud_lister, sample_log_lines):
    """Test getting a sorted list of event cruds."""
    log_line_1 = sample_log_lines.make_insert_log_line()
    meetup_id_1 = log_line_1.meetup_id
    crud_lister.add_log_line(log_line_1)
    log_line_2 = sample_log_lines.make_delete_log_line()
    meetup_id_2 = log_line_2.meetup_id
    crud_lister.add_log_line(log_line_2)
    log_line_3 = sample_log_lines.make_update_log_line()
    meetup_id_3 = log_line_3.meetup_id
    crud_lister.add_log_line(log_line_3)
    crud_list = crud_lister.sorted_event_cruds()
    meetup_ids = [crud.final_event.meetup_id for crud in crud_list]
    assert meetup_ids == [meetup_id_2, meetup_id_3, meetup_id_1]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

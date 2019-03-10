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
    date_time = sample_log_lines.date_time()
    fields = sample_log_lines.insert_fields
    crud_lister.add_insert_event(date_time, fields)

def test_add_update_event(crud_lister, sample_log_lines):
    """Test adding an update event log line to the lister."""
    date_time = sample_log_lines.date_time()
    before_fields = sample_log_lines.update_before_fields
    after_fields = sample_log_lines.update_after_fields
    crud_lister.add_update_event(date_time, before_fields, after_fields)

def test_add_delete_event(crud_lister, sample_log_lines):
    """Test adding a delete event log line to the lister."""
    date_time = sample_log_lines.date_time()
    fields = sample_log_lines.delete_fields
    crud_lister.add_delete_event(date_time, fields)




# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

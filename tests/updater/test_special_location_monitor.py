"""Test logging unneeded special locations."""

from meetup2xibo.updater.special_location import SpecialLocation
from meetup2xibo.updater.special_location_monitor import SpecialLocationMonitor
from meetup2xibo.updater.xibo_event import XiboEvent
import logging
import pytest

SAMPLE_MEETUP_ID = "A123"
SAMPLE_LOCATION = "Room 1"

SAMPLE_XIBO_EVENT = XiboEvent(
    meetup_id = SAMPLE_MEETUP_ID,
    xibo_id = "1234",
    name = "Nova Labs Open House",
    location = "Orange Bay",
    start_time = "2018-02-10 15:00:00",
    end_time = "2018-02-10 17:00:00"
)

def make_special_location(meetup_id=SAMPLE_MEETUP_ID, location=SAMPLE_LOCATION,
        override=False, comment="", places=[]):
    """Return a special location configured as needed."""
    return SpecialLocation (meetup_id, location, override, comment, places)

def has_warnings(log_records):
    """Test whether any log record is a warning."""
    return "WARNING" in [record.levelname for record in log_records]

def test_deleted_event_with_special_location(caplog):
    """Test logging the special location for a deleted Xibo event."""
    caplog.set_level(logging.INFO)
    special_location = make_special_location()
    special_location_dict = {SAMPLE_MEETUP_ID: special_location}
    special_location_monitor = SpecialLocationMonitor(special_location_dict)
    special_location_monitor.deleted_event(SAMPLE_XIBO_EVENT)
    assert "No longer needed" in caplog.text

def test_deleted_event_no_special_location(caplog):
    """Test not logging a deleted Xibo event with no special location."""
    caplog.set_level(logging.INFO)
    special_location_dict = {}
    special_location_monitor = SpecialLocationMonitor(special_location_dict)
    special_location_monitor.deleted_event(SAMPLE_XIBO_EVENT)
    assert "No longer needed" not in caplog.text

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

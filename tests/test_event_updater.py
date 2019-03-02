"""Tests for the event updater."""

from .context import meetup2xibo
from meetup2xibo.event_converter import Event
from meetup2xibo.xibo_event import XiboEvent
from meetup2xibo.event_updater import EventUpdater
from meetup2xibo.anti_flapper import AntiFlapper
from unittest.mock import MagicMock, call


# New event
NEW_MEETUP_EVENT = Event("A01", "Sewing Class", "Crafter's Corner", "2017-12-12 19:00:00", "2017-12-11 21:00:00")

# Updated event
UPDATED_MEETUP_EVENT = Event("B01", "Metal Class", "Room 1", "2017-12-11 19:00:00", "2017-12-11 21:00:00")
UPDATED_XIBO_EVENT = XiboEvent(101, "B01", "Metal Class", "Metal Shop", "2017-12-11 19:15:00", "2017-12-11 21:00:00")

# Unchanged event
UNCHANGED_MEETUP_EVENT = Event("C01", "Wood Class", "Room 2", "2017-12-11 19:30:00", "2017-12-11 21:30:00")
UNCHANGED_XIBO_EVENT = XiboEvent(102, "C01", "Wood Class", "Room 2", "2017-12-11 19:30:00", "2017-12-11 21:30:00")

# Deleted event past
DELETED_PAST_XIBO_EVENT = XiboEvent(103, "D01", "Lathe Class", "Room 3", "2017-12-09 18:00:00", "2017-12-09 22:00:00")

# Deleted event current
DELETED_CURRENT_XIBO_EVENT = XiboEvent(104, "D02", "Laser Class", "Room 4", "2017-12-11 20:00:00", "2017-12-11 23:00:00")

# Deleted event future
DELETED_FUTURE_XIBO_EVENT = XiboEvent(105, "D03", "Casting Class", "Room 5", "2017-12-13 17:00:00", "2017-12-13 19:00:00")


MEETUP_EVENTS = [NEW_MEETUP_EVENT, UNCHANGED_MEETUP_EVENT, UPDATED_MEETUP_EVENT]
XIBO_EVENTS = [UPDATED_XIBO_EVENT, DELETED_PAST_XIBO_EVENT,
    DELETED_CURRENT_XIBO_EVENT, UNCHANGED_XIBO_EVENT, DELETED_FUTURE_XIBO_EVENT]

EXPECTED_MEETUP_EVENTS_DICT = {
    "A01": NEW_MEETUP_EVENT,
    "B01": UPDATED_MEETUP_EVENT,
    "C01": UNCHANGED_MEETUP_EVENT
}

EXPECTED_XIBO_EVENTS_DICT = {
    "B01": UPDATED_XIBO_EVENT,
    "C01": UNCHANGED_XIBO_EVENT,
    "D01": DELETED_PAST_XIBO_EVENT,
    "D02": DELETED_CURRENT_XIBO_EVENT,
    "D03": DELETED_FUTURE_XIBO_EVENT,
}


def test_event_list_to_dict():
    """Test creating a dictionary indexec by Meetup ID from a list of events."""
    assert EXPECTED_MEETUP_EVENTS_DICT == EventUpdater.event_list_to_dict(MEETUP_EVENTS)

def test_init():
    """Test converting event lists to dictionaries during initialization."""
    event_updater = EventUpdater(MEETUP_EVENTS, XIBO_EVENTS, None, None)
    assert EXPECTED_MEETUP_EVENTS_DICT == event_updater.meetup_events
    assert EXPECTED_XIBO_EVENTS_DICT == event_updater.xibo_events

def test_insert_new_events():
    """Test inserting new events."""
    mock_xibo_event_crud = MagicMock()
    event_updater = EventUpdater(MEETUP_EVENTS, XIBO_EVENTS, mock_xibo_event_crud, None)
    insert_ids = {"A01", "C01"}
    event_updater.insert_new_events(insert_ids)
    calls = [call(NEW_MEETUP_EVENT), call(UNCHANGED_MEETUP_EVENT)]
    mock_xibo_event_crud.insert_meetup_event.assert_has_calls(calls, any_order = True)

def test_update_known_events():
    """Test updating known events."""
    mock_xibo_event_crud = MagicMock()
    event_updater = EventUpdater(MEETUP_EVENTS, XIBO_EVENTS, mock_xibo_event_crud, None)
    update_ids = {"B01", "C01"}
    event_updater.update_known_events(update_ids)
    calls = [call(UPDATED_XIBO_EVENT, UPDATED_MEETUP_EVENT)]
    mock_xibo_event_crud.update_xibo_event.assert_has_calls(calls, any_order = True)

def test_delete_unknown_events():
    """Test deleting unknown events."""
    anti_flapper = AntiFlapper("2017-12-11 19:00:00", "2017-12-11 22:00:00", "2017-12-31 23:00:00")
    mock_xibo_event_crud = MagicMock()
    event_updater = EventUpdater(MEETUP_EVENTS, XIBO_EVENTS, mock_xibo_event_crud, anti_flapper)
    delete_ids = {"D01", "D02", "D03"}
    event_updater.delete_unknown_events(delete_ids)
    calls = [
        call(DELETED_PAST_XIBO_EVENT),
        call(DELETED_FUTURE_XIBO_EVENT),
    ]
    mock_xibo_event_crud.delete_xibo_event.assert_has_calls(calls, any_order = True)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

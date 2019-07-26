"""Test choosing locations for a Meetup event."""

from meetup2xibo.updater.application_scope import SpecialLocation
from meetup2xibo.updater.event_converter import PartialEvent
from meetup2xibo.updater.event_location import EventLocation
from meetup2xibo.updater.location_chooser import LocationChooser
import logging
import pytest


SAMPLE_MEETUP_ID = "A123"

SAMPLE_DEFAULT_LOCATION = "Lobby"
SAMPLE_DEFAULT_EVENT_LOCATION = EventLocation(SAMPLE_DEFAULT_LOCATION, [])

LOCATION_1 = "Room 1"
EVENT_LOCATION_1 = EventLocation(LOCATION_1, [LOCATION_1])

LOCATION_2 = "Theater"
EVENT_LOCATION_2 = EventLocation(LOCATION_2, [LOCATION_2])

NO_EVENT_LOCATION = EventLocation("", [])


@pytest.fixture
def minimal_location_chooser():
    """Return a location chooser with nothing but the sample default
    location."""
    return LocationChooser(None, None, SAMPLE_DEFAULT_EVENT_LOCATION)

def make_partial_event(venue_name = "", find_us = "", name = "Some Event"):
    """Return a partial event with some test values."""
    return PartialEvent(
        SAMPLE_MEETUP_ID, name, "2019-03-01 19:00:00", "2019-03-01 21:00:00",
        venue_name, find_us)

def make_special_location(meetup_id=SAMPLE_MEETUP_ID,
        location=LOCATION_2, override=False, comment="", places=[LOCATION_2]):
    """Return a special location configured as needed."""
    return SpecialLocation (meetup_id, location, override, comment, places)

def has_warnings(log_records):
    """Test whether any log record is a warning."""
    return "WARNING" in [record.levelname for record in log_records]

def test_resolve_locations_no_locations(minimal_location_chooser, caplog):
    """Test returning the default location when there is neither a computed
    location nor a special location."""
    caplog.set_level(logging.INFO)
    partial_event = make_partial_event()
    location =  minimal_location_chooser.resolve_locations(partial_event, "", None)
    assert location == SAMPLE_DEFAULT_EVENT_LOCATION
    assert "Unknown location" in caplog.text

def test_resolve_locations_event_location(minimal_location_chooser, caplog):
    """Test returning the default location when there is a computed location
    and no special location."""
    caplog.set_level(logging.INFO)
    partial_event = make_partial_event(LOCATION_1)
    location =  minimal_location_chooser.resolve_locations(partial_event, EVENT_LOCATION_1, None)
    assert location == EVENT_LOCATION_1
    assert "Unknown location" not in caplog.text

def test_resolve_locations_special_no_locations(minimal_location_chooser, caplog):
    """Test returning the default location when there is no computed
    location and a special location without a location."""
    caplog.set_level(logging.INFO)
    partial_event = make_partial_event()
    special_location = make_special_location(location = "")
    location =  minimal_location_chooser.resolve_locations(partial_event, "", special_location)
    assert location == SAMPLE_DEFAULT_EVENT_LOCATION
    assert "Unknown location" not in caplog.text

def test_resolve_locations_special_location(minimal_location_chooser, caplog):
    """Test returning the default location when there is no computed
    location and a special location with a location."""
    caplog.set_level(logging.INFO)
    partial_event = make_partial_event()
    special_location = make_special_location()
    event_location =  minimal_location_chooser.resolve_locations(partial_event, "", special_location)
    assert event_location == EVENT_LOCATION_2
    assert "Unknown location" not in caplog.text

def test_resolve_locations_both_locations_no_override(minimal_location_chooser, caplog):
    """Test returning the default location when there is a computed location
    and a special location with a location, but no override."""
    caplog.set_level(logging.INFO)
    partial_event = make_partial_event(LOCATION_1)
    special_location = make_special_location()
    location =  minimal_location_chooser.resolve_locations(partial_event, EVENT_LOCATION_1, special_location)
    assert location == EVENT_LOCATION_1
    assert "Unknown location" not in caplog.text

def test_resolve_locations_both_locations_override(minimal_location_chooser, caplog):
    """Test returning the default location when there is a computed location
    and a special location with a location and an override."""
    caplog.set_level(logging.INFO)
    partial_event = make_partial_event(LOCATION_1)
    special_location = make_special_location(override = True)
    location =  minimal_location_chooser.resolve_locations(partial_event, LOCATION_1, special_location)
    assert location == EVENT_LOCATION_2
    assert "Unknown location" not in caplog.text

def test_find_event_location_known(place_finder):
    """Test finding a known location from an event's venue name and "how to
    find us" information."""
    partial_event = make_partial_event("Metalshop", "[Classroom A]")
    location_chooser = LocationChooser(place_finder, {}, SAMPLE_DEFAULT_EVENT_LOCATION)
    event_location = location_chooser.find_event_location(partial_event)
    expected_event_location = EventLocation(
            "Metal Shop and Classroom A",
            ["Metal Shop", "Classroom A"])
    assert event_location == expected_event_location

def test_find_event_location_unknown(place_finder):
    """Test finding an unknown location from an event's venue name and "how to
    find us" information."""
    partial_event = make_partial_event("Orange Bay")
    location_chooser = LocationChooser(place_finder, {}, SAMPLE_DEFAULT_EVENT_LOCATION)
    event_location = location_chooser.find_event_location(partial_event)
    expected_event_location = NO_EVENT_LOCATION
    assert event_location == expected_event_location

def test_choose_location_computed(place_finder, caplog):
    """Test choosing a location from an event's venue name and "how to
    find us" information when there is no special location."""
    caplog.set_level(logging.INFO)
    partial_event = make_partial_event("Metal Shop")
    location_chooser = LocationChooser(place_finder, {}, SAMPLE_DEFAULT_EVENT_LOCATION)
    location = location_chooser.choose_location(partial_event)
    expected_event_location = EventLocation("Metal Shop", ["Metal Shop"])
    assert location == expected_event_location
    assert "Unknown location" not in caplog.text

def test_choose_location_special(place_finder, caplog):
    """Test choosing a location from an event's venue name and "how to
    find us" information when there is a special location."""
    partial_event = make_partial_event("Metal Shop")
    special_location = make_special_location(override = True)
    special_location_dict = {SAMPLE_MEETUP_ID: special_location}
    location_chooser = LocationChooser(place_finder, special_location_dict,
            SAMPLE_DEFAULT_EVENT_LOCATION)
    location = location_chooser.choose_location(partial_event)
    assert location == EVENT_LOCATION_2
    assert not has_warnings(caplog.records)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

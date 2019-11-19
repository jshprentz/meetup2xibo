"""Test the event converter from Meetup JSON to event object."""

from meetup2xibo.updater.event_converter import EventListConverter, Event
from meetup2xibo.updater.event_suppressor import EventSuppressor
import pytest


JSON_EVENT1 = {
    "duration": 8100000,
    "how_to_find_us": "Nova Labs",
    "id": "zvbxrpl",
    "name": "Computational Mathematics: P=NP for students and engineers",
    "time": 1511223300000,
    "venue": {
        "name": "*Nova Labs (Conference Rm 2)"
    }
}

EVENT1 = Event(
    meetup_id = "zvbxrpl",
    name = "Computational Mathematics: P=NP for students and engineers",
    start_time = "2017-11-20 19:15:00",
    end_time = "2017-11-20 21:30:00",
    places = ["Conference Room 2"],
    location = "Conference Room 2")

JSON_EVENT2 = {
    "duration": 8100000,
    "how_to_find_us": "Nova Labs",
    "id": "lsmft",
    "name": "Wood Lathe Sign Off",
    "time": 1511223300000,
    "venue": {
        "name": "Woodshop"
    }
}

EVENT2 = Event(
    meetup_id = "lsmft",
    name = "Wood Lathe Sign Off",
    start_time = "2017-11-20 19:15:00",
    end_time = "2017-11-20 21:30:00",
    places = ["Woodshop"],
    location = "Woodshop")

JSON_EVENTS = [JSON_EVENT1, JSON_EVENT2]
ALL_EVENTS = [EVENT1, EVENT2]


def assert_convert_meetup_events(mocker, event_suppressor,
        expected_json_events, expected_events):
    """Assert that expected events and JSON events result from converting JSON
    Meetup events with an event suppressor."""
    return_events = expected_events + [None, None]
    event_converter = mocker.Mock()
    event_converter.convert = mocker.Mock(side_effect = return_events)
    expected_calls = map(mocker.call, expected_json_events)
    converter = EventListConverter(event_converter, event_suppressor)
    assert converter.convert_meetup_events(JSON_EVENTS) == expected_events
    event_converter.convert.assert_has_calls(expected_calls)

def assert_convert_cancelled_meetup_events(mocker, event_suppressor,
        expected_json_events, expected_events):
    """Assert that expected events and JSON events result from converting
    cancelled JSON Meetup events with an event suppressor."""
    return_events = expected_events + [None, None]
    event_converter = mocker.Mock()
    event_converter.convert_cancelled = mocker.Mock(side_effect = return_events)
    expected_calls = map(mocker.call, expected_json_events)
    converter = EventListConverter(event_converter, event_suppressor)
    assert converter.convert_cancelled_meetup_events(JSON_EVENTS) == expected_events
    event_converter.convert_cancelled.assert_has_calls(expected_calls)

def test_convert_meetup_events_all(mocker):
    """Test converting all meetup events when none are suppressed."""
    event_suppressor = EventSuppressor([])
    assert_convert_meetup_events(mocker, event_suppressor,
        JSON_EVENTS, ALL_EVENTS)

def test_convert_meetup_events_one(mocker):
    """Test converting one meetup event when one is suppressed."""
    event_suppressor = EventSuppressor(["zvbxrpl"])
    assert_convert_meetup_events(mocker, event_suppressor,
        [JSON_EVENT2], [EVENT2])

def test_convert_cancelled_meetup_events_all(mocker):
    """Test converting all cancelled meetup events when none are suppressed."""
    event_suppressor = EventSuppressor([])
    assert_convert_cancelled_meetup_events(mocker, event_suppressor,
        JSON_EVENTS, ALL_EVENTS)

def test_convert_cancelled_meetup_events_one(mocker):
    """Test converting one cancelled meetup event when one is suppressed."""
    event_suppressor = EventSuppressor(["lsmft"])
    assert_convert_cancelled_meetup_events(mocker, event_suppressor,
        [JSON_EVENT1], [EVENT1])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

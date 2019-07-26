"""Test the anti-flapper's judgements about event times."""

from meetup2xibo.updater.conflict_analyzer import ConflictAnalyzer
from meetup2xibo.updater.conflict_places import ConflictPlaces
from meetup2xibo.updater.event_converter import Event
from meetup2xibo.updater.exceptions import ContainmentLoopError
from hypothesis import given, assume, example
from .sample_events import SampleEvents
import pytest
import hypothesis.strategies as st
from datetime import datetime
import string
import logging

MINIMUM_TEST_DATE = datetime(2019, 1, 1, 0, 0, 0)
MAXIMUM_TEST_DATE = datetime(2029, 12, 31, 23, 59, 59)

def iso_format(the_date_time):
    """Format a date/time in ISO YYYY-MM-DD hh:mm:ss format."""
    return the_date_time.strftime('%Y-%m-%d %H:%M:%S')

typical_dates = st.datetimes(min_value = MINIMUM_TEST_DATE, max_value = MAXIMUM_TEST_DATE)

iso_dates = typical_dates.map(iso_format)

meetup_ids = st.text(alphabet = string.ascii_lowercase, min_size = 3, max_size = 3)

small_list_sizes = st.integers(min_value = 0, max_value = 4)

sortable_events = st.builds(
        Event,
        meetup_id = meetup_ids,
        name = st.just("Some Event"),
        start_time = iso_dates,
        end_time = iso_dates,
        places = st.just(["Conference Room 2"]),
        location = st.just("Conference Room 2"))

sortable_events_lists = st.lists(
        sortable_events,
        max_size=6,
        unique_by = lambda event: event.meetup_id)


@pytest.fixture
def conflict_places():
    """Return a populated conflict places."""
    conflict_places = ConflictPlaces()
    conflict_places.add_checked_place("Woodshop")
    conflict_places.add_checked_place("Metal Shop")
    conflict_places.add_checked_place("Classroom A")
    conflict_places.add_checked_place("Classroom B")
    conflict_places.add_checked_place("Classroom A/B")
    conflict_places.add_containing_place("Shops", ["Woodshop", "Metal Shop", "Storeroom"])
    conflict_places.add_containing_place("Classroom A/B", ["Classroom A", "Classroom B"])
    return conflict_places

@pytest.fixture
def conflict_analyzer(conflict_places):
    """Return a conflict analyzer for the conflict places."""
    return ConflictAnalyzer(conflict_places)

@given(sortable_events_lists)
@example(SampleEvents().make_sample_sortable_events())
def test_events_by_start_time(events):
    """Test sorting events by start time."""
    sorted_events = ConflictAnalyzer.events_by_start_time(events)
    assert len(events) == len(sorted_events)
    for i in range(0, len(sorted_events) - 1):
        if sorted_events[i].start_time == sorted_events[i + 1].start_time:
            assert sorted_events[i].meetup_id > sorted_events[i + 1].meetup_id
        else:
            assert sorted_events[i].start_time > sorted_events[i + 1].start_time

@given(sortable_events_lists)
@example(SampleEvents().make_sample_sortable_events())
def test_events_by_end_time(events):
    """Test sorting events by end time."""
    sorted_events = ConflictAnalyzer.events_by_end_time(events)
    assert len(events) == len(sorted_events)
    for i in range(0, len(sorted_events) - 1):
        if sorted_events[i].end_time == sorted_events[i + 1].end_time:
            assert sorted_events[i].meetup_id > sorted_events[i + 1].meetup_id
        else:
            assert sorted_events[i].end_time > sorted_events[i + 1].end_time

@given(early_list_size = small_list_sizes, late_list_size = small_list_sizes)
def test_analyze_events_at_start_time(early_list_size, late_list_size, sample_events, mocker):
    """Test analyzing event starts from a list ordered by start time. (Tested
    before conflict places was implemented.)"""
    early_events = sample_events.make_early_events(early_list_size)
    if early_events:
        start_time = early_events[0].start_time
    else:
        start_time = "2016-01-01 11:22:33"
    late_events = sample_events.make_late_events(late_list_size)
    expected_calls = [mocker.call(event) for event in early_events]
    conflict_places = mocker.Mock()
    conflict_analyzer = ConflictAnalyzer(conflict_places)
    sorted_events = conflict_analyzer.events_by_start_time(early_events + late_events)
    conflict_analyzer.analyze_events_at_start_time(sorted_events, start_time)
    assert conflict_places.start_event.call_args_list == expected_calls
    for remaining_event in late_events:
        assert remaining_event == sorted_events.pop()
    assert not sorted_events

@given(early_list_size = small_list_sizes, late_list_size = small_list_sizes)
def test_analyze_events_at_end_time(early_list_size, late_list_size, sample_events, mocker):
    """Test analyzing event ends from a list ordered by end time. (Tested
    before conflict places was implemented.)"""
    early_events = sample_events.make_early_events(early_list_size)
    if early_events:
        end_time = early_events[0].end_time
    else:
        end_time = "2016-01-01 11:22:33"
    late_events = sample_events.make_late_events(late_list_size)
    expected_calls = [mocker.call(event) for event in early_events]
    conflict_places = mocker.Mock()
    conflict_analyzer = ConflictAnalyzer(conflict_places)
    sorted_events = conflict_analyzer.events_by_end_time(early_events + late_events)
    conflict_analyzer.analyze_events_at_end_time(sorted_events, end_time)
    assert conflict_places.end_event.call_args_list == expected_calls
    for remaining_event in late_events:
        assert remaining_event == sorted_events.pop()
    assert not sorted_events

@given(sortable_events_lists)
def test_earliest_time(events):
    """Test finding the earliest start or end time."""
    assume(events)
    earliest_time = "9999-99-99 99:99:99"
    for event in events:
        earliest_time = min(earliest_time, event.start_time, event.end_time)
    events_sorted_by_start = ConflictAnalyzer.events_by_start_time(events)
    events_sorted_by_end = ConflictAnalyzer.events_by_end_time(events)
    assert earliest_time == ConflictAnalyzer.earliest_time(
            events_sorted_by_start, events_sorted_by_end)

def assert_overlap_conflict(message, event1, event2, place):
    """Assert that a log message describes an overlap conflict between two
    events at a place."""
    assert_conflict(message, place, event2.start_time, event1.end_time,
            [event1.meetup_id, event2.meetup_id])

def assert_conflict(message, expected_place, expected_start_time,
        expected_end_time, expected_meetup_ids):
    """Assert that a log message describes a conflict with the expected place,
    times, and message IDs."""
    assert "Schedule conflict: place='{}'".format(expected_place) in message
    expected_conflict_times = "Conflict(start_time='{}', end_time='{}',".format(
            expected_start_time, expected_end_time)
    assert expected_conflict_times in message
    for meetup_id in expected_meetup_ids:
        assert meetup_id in message

def test_overlapping_events_checked_place(sample_events, conflict_analyzer, caplog):
    """Test analyzing overlapping events in a checked place."""
    caplog.set_level(logging.INFO)
    places = ["Woodshop"]
    event1, event2 = sample_events.make_overlapping_events(places)
    conflict_analyzer.sort_and_analyze_events([event1, event2])
    assert len(caplog.messages) == 1
    assert_overlap_conflict(caplog.messages[0], event1, event2, "Woodshop")

def test_overlapping_events_checked_containing_place(sample_events,
        conflict_analyzer, caplog):
    """Test analyzing overlapping events in a checked place that contains other
    checked places."""
    caplog.set_level(logging.INFO)
    places = ["Classroom A/B"]
    event1, event2 = sample_events.make_overlapping_events(places)
    conflict_analyzer.sort_and_analyze_events([event1, event2])
    assert len(caplog.messages) == 1
    assert_overlap_conflict(caplog.messages[0], event1, event2, "Classroom A/B")

def test_overlapping_events_unchecked_containing_place(sample_events,
        conflict_analyzer, caplog):
    """Test analyzing overlapping events in an unchecked place that contains
    checked and unchecked places."""
    caplog.set_level(logging.INFO)
    places = ["Shops"]
    event1, event2 = sample_events.make_overlapping_events(places)
    conflict_analyzer.sort_and_analyze_events([event1, event2])
    assert len(caplog.messages) == 2
    messages = sorted(caplog.messages)
    assert_overlap_conflict(messages[0], event1, event2, "Metal Shop")
    assert_overlap_conflict(messages[1], event1, event2, "Woodshop")

def test_multiple_overlapping_events(sample_events, conflict_analyzer,
        caplog):
    """Test analyzing a four events with overlaps in a checked places."""
    caplog.set_level(logging.INFO)
    place = "Classroom A"
    event1, event2 = sample_events.make_overlapping_events([place])
    event3, event4 = sample_events.make_overlapping_events([place])
    conflict_analyzer.sort_and_analyze_events([event1, event3, event2, event4])
    assert len(caplog.messages) == 3
    assert_conflict(caplog.messages[0], place, event1.start_time,
            event2.start_time, [event1.meetup_id, event3.meetup_id])
    assert_conflict(caplog.messages[1], place, event2.start_time, event1.end_time,
            [event1.meetup_id, event2.meetup_id, event3.meetup_id, event4.meetup_id])
    assert_conflict(caplog.messages[2], place, event1.end_time,
            event2.end_time, [event2.meetup_id, event4.meetup_id])

def test_overlapping_events_from_sequence(sample_events, conflict_analyzer,
        caplog):
    """Test analyzing a sequence of events with overlaps in a checked places."""
    caplog.set_level(logging.INFO)
    event1, event2 = sample_events.make_same_start_events(["Classroom A"])
    event3, event4 = sample_events.make_same_end_events(["Classroom A/B"])
    conflict_analyzer.sort_and_analyze_events([event1, event3, event2, event4])
    assert len(caplog.messages) == 3
    assert_overlap_conflict(caplog.messages[0], event1, event1, "Classroom A")
    assert_overlap_conflict(caplog.messages[1], event2, event3, "Classroom A")
    assert_overlap_conflict(caplog.messages[2], event4, event4, "Classroom A/B")

def test_analyzing_containment_loops(sample_events, conflict_places,
        conflict_analyzer, caplog):
    """Test analyzing an event in a place that contains a place that contains
    the first place.."""
    caplog.set_level(logging.INFO)
    conflict_places.add_containing_place("Storeroom", ["Shops"])
    try:
        sample_events.make_overlapping_events(["Storeroom"])
    except ContainmentLoopError as err:
        assert str(err) == "Loop found among containing places. Check 'Storeroom'."

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Test the anti-flapper's judgements about event times."""

from meetup2xibo.updater.conflict_analyzer import ConflictAnalyzer
from meetup2xibo.updater.event_converter import Event
from hypothesis import given, assume, example
from .sample_events import SampleEvents
import hypothesis.strategies as st
from datetime import datetime
import string

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

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

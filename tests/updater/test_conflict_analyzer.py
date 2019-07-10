"""Test the anti-flapper's judgements about event times."""

from meetup2xibo.updater.conflict_analyzer import ConflictAnalyzer
from meetup2xibo.updater.event_converter import Event
from hypothesis import given, assume, example
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
meetup_ids = st.text(alphabet = string.ascii_lowercase, min_size = 6, max_size = 6)
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
def test_events_by_start_time(events):
    """Test sorting events by start time."""
    sorted_events = ConflictAnalyzer.events_by_start_time(events)
    assert len(events) == len(sorted_events)
    for i in range(0, len(sorted_events) - 1):
        assert sorted_events[i].start_time < sorted_events[i + 1].start_time or (
                sorted_events[i].start_time == sorted_events[i + 1].start_time
                and
                sorted_events[i].meetup_id < sorted_events[i + 1].meetup_id)

@given(sortable_events_lists)
def test_events_by_end_time(events):
    """Test sorting events by end time."""
    sorted_events = ConflictAnalyzer.events_by_end_time(events)
    assert len(events) == len(sorted_events)
    for i in range(0, len(sorted_events) - 1):
        assert sorted_events[i].end_time < sorted_events[i + 1].end_time or (
                sorted_events[i].end_time == sorted_events[i + 1].end_time
                and
                sorted_events[i].meetup_id < sorted_events[i + 1].meetup_id)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Test conflict comparison and reporting."""

from meetup2xibo.log_summarizer.conflict import Conflict
from meetup2xibo.log_summarizer.event import Event
import pytest
from hypothesis import given, assume, example
import hypothesis.strategies as st
from datetime import datetime

SAMPLE_MEETUP_ID = 'qlpqsqyzhbqb'
SAMPLE_NAME = 'Arduino User Group'
SAMPLE_LOCATION = 'Conference Room 3'
SAMPLE_START_TIME = '2019-05-12 15:00:00'
SAMPLE_END_TIME = '2019-05-12 17:00:00'

SAMPLE_OTHER_MEETUP_ID = '75636384'
SAMPLE_OTHER_NAME = 'Tech Toastmasters'

MINIMUM_TEST_DATE = datetime(2019, 1, 1, 0, 0, 0)
MAXIMUM_TEST_DATE = datetime(2029, 12, 31, 23, 59, 59)

def iso_format(the_date_time):
    """Format a date/time in ISO YYYY-MM-DD hh:mm:ss format."""
    return the_date_time.strftime('%Y-%m-%d %H:%M:%S')

typical_dates = st.datetimes(min_value = MINIMUM_TEST_DATE, max_value = MAXIMUM_TEST_DATE)
iso_dates = typical_dates.map(iso_format)


def make_event(
        name=SAMPLE_NAME,
        location=SAMPLE_LOCATION,
        start_time=SAMPLE_START_TIME,
        end_time=SAMPLE_END_TIME,
        meetup_id=SAMPLE_MEETUP_ID):
    """Make an event with default sample values."""
    return Event(name, start_time, end_time, meetup_id, location)

def make_conflict(
        start_time=SAMPLE_START_TIME,
        end_time=SAMPLE_END_TIME,
        events=None):
    """Make a conflict with default sample values."""
    return Conflict(
        start_time, end_time,
        events or [
            make_event(),
            make_event(name=SAMPLE_OTHER_NAME, meetup_id=SAMPLE_OTHER_MEETUP_ID)
            ])

def test_equals_identical():
    """Test comparing an conflict with it self."""
    conflict = make_conflict()
    assert conflict == conflict

def test_equals_same():
    """Test comparing conflicts with the same value."""
    conflict1 = make_conflict()
    conflict2 = make_conflict()
    assert conflict1 == conflict2

def test_equals_different_start_times():
    """Test comparing conflicts with different start times."""
    conflict1 = make_conflict()
    conflict2 = make_conflict(start_time="2019-05-12 10:00:00")
    assert conflict1 != conflict2

def test_equals_different_end_times():
    """Test comparing conflicts with different end times."""
    conflict1 = make_conflict()
    conflict2 = make_conflict(end_time="2019-05-12 19:00:00")
    assert conflict1 != conflict2

def test_equals_different_events():
    """Test comparing conflicts with different events."""
    conflict1 = make_conflict()
    conflict2 = make_conflict(events=[
            make_event(),
            make_event(name="Arduino 101", meetup_id="abcdygyghej")
            ])
    assert conflict1 != conflict2

def test_equals_non_event():
    """Test comparing an conflict with a non-event."""
    event = make_conflict()
    assert event != "foo"

def test_hash_identical():
    """Test that an conflict hash is always the same."""
    event = make_conflict()
    assert hash(event) == hash(event)

def test_hash_same():
    """Test that two conflicts with the same values hash the same."""
    conflict1 = make_conflict()
    conflict2 = make_conflict()
    assert hash(conflict1) == hash(conflict2)

@given(iso_dates)
def test_hash_different_start_times(other_start_time):
    """Test hashing conflicts with different start_times."""
    assume(other_start_time != SAMPLE_START_TIME)
    conflict1 = make_conflict()
    conflict2 = make_conflict(start_time=other_start_time)
    assert hash(conflict1) != hash(conflict2)

@given(iso_dates)
def test_hash_different_end_times(other_end_time):
    """Test hashing conflicts with different end_times."""
    assume(other_end_time != SAMPLE_END_TIME)
    conflict1 = make_conflict()
    conflict2 = make_conflict(end_time=other_end_time)
    assert hash(conflict1) != hash(conflict2)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Test the anti-flapper's judgements about event times."""

from .context import meetup2xibo
from meetup2xibo.xibo_event import XiboEvent
from meetup2xibo.anti_flapper import AntiFlapper, iso_offset_time
from hypothesis import given, assume, example
import hypothesis.strategies as st
from datetime import datetime

MINIMUM_TEST_DATE = datetime(2019, 1, 1, 0, 0, 0)
MAXIMUM_TEST_DATE = datetime(2029, 12, 31, 23, 59, 59)

def iso_format(the_date_time):
    """Format a date/time in ISO YYYY-MM-DD hh:mm:ss format."""
    return the_date_time.strftime('%Y-%m-%d %H:%M:%S')

typical_dates = st.datetimes(min_value = MINIMUM_TEST_DATE, max_value = MAXIMUM_TEST_DATE)
iso_dates = typical_dates.map(iso_format)
iso_date_lists = st.lists(iso_dates, min_size = 5, max_size = 5, unique = True).map(sorted)

def make_xibo_event(start_time, end_time):
    """Return a Xibo event with the start and end times."""
    return XiboEvent(
        xibo_id = "456",
        meetup_id = "zvbxrpl",
        name = "Nova Labs Open House",
        location = "Orange Bay",
        start_time = start_time,
        end_time = end_time
        )

def assert_event_ok(event_start, event_end, recent, current, future):
    """Assert that an event with start and end times falls outside the flapping windows."""
    anti_flapper = AntiFlapper(recent, current, future)
    xibo_event = make_xibo_event(event_start, event_end)
    assert anti_flapper.is_ok(xibo_event)

def assert_event_not_ok(event_start, event_end, recent, current, future):
    """Assert that an event with start and end times does not fall outside the
    flapping windows."""
    anti_flapper = AntiFlapper(recent, current, future)
    xibo_event = make_xibo_event(event_start, event_end)
    assert not anti_flapper.is_ok(xibo_event)

@given(iso_dates = iso_date_lists)
def test_past_event_ok(iso_dates):
    """Test that an event ending before flapping windows is ok."""
    event_start, event_end, recent, current, future = tuple(iso_dates)
    assert_event_ok(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_recent_event_ok(iso_dates):
    """Test that an event ending during the recent to current flapping windows is not ok."""
    event_start, recent, event_end, current, future = tuple(iso_dates)
    assert_event_not_ok(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_current_event_ok(iso_dates):
    """Test that an event within the recent to current flapping windows is not ok."""
    recent, event_start, event_end, current, future = tuple(iso_dates)
    assert_event_not_ok(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_ongoing_event_ok(iso_dates):
    """Test that an event starting within the recent to current flapping windows is not ok."""
    recent, event_start, current, event_end, future = tuple(iso_dates)
    assert_event_not_ok(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_surrounding_event_ok(iso_dates):
    """Test that an event surrounding the recent to current flapping windows is not ok."""
    event_start, recent, current, event_end, future = tuple(iso_dates)
    assert_event_not_ok(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_planned_event_ok(iso_dates):
    """Test that an event planned between the flapping windows is ok."""
    recent, current, event_start, event_end, future = tuple(iso_dates)
    assert_event_ok(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_future_event_ok(iso_dates):
    """Test that a future event ending after the future time is not ok."""
    recent, current, event_start, future, event_end = tuple(iso_dates)
    assert_event_not_ok(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_far_future_event_ok(iso_dates):
    """Test that a future event starting after the future time is not ok."""
    recent, current, future, event_start, event_end = tuple(iso_dates)
    assert_event_not_ok(event_start, event_end, recent, current, future)

def test_iso_offset_time_future():
    """Test offsetting time into the future."""
    now = datetime(2019, 2, 28, 23, 0, 0)
    assert iso_offset_time(now, 4500) == "2019-03-01 00:15:00"

def test_iso_offset_time_past():
    """Test offsetting time into the past."""
    now = datetime(2019, 2, 28, 23, 0, 0)
    assert iso_offset_time(now, -4500) == "2019-02-28 21:45:00"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

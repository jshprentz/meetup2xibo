"""Test the anti-flapper's judgements about event times."""

from meetup2xibo.updater.xibo_event import XiboEvent
from meetup2xibo.updater.anti_flapper import AntiFlapper, EventFlappingStatus
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

def assert_event_status(status, event_start, event_end, recent, current, future):
    """Assert that an event with start and end times has the expected status
    relative to the flapping windows."""
    anti_flapper = AntiFlapper(recent, current, future)
    xibo_event = make_xibo_event(event_start, event_end)
    assert anti_flapper.categorize(xibo_event) == status

def assert_event_retire(event_start, event_end, recent, current, future):
    """Assert retiring an event with start and end times relative to the
    flapping windows."""
    status = EventFlappingStatus.retire
    assert_event_status(status, event_start, event_end, recent, current, future)

def assert_event_delete(event_start, event_end, recent, current, future):
    """Assert deleting an event with start and end times relative to the
    flapping windows."""
    status = EventFlappingStatus.delete
    assert_event_status(status, event_start, event_end, recent, current, future)

def assert_event_keep(event_start, event_end, recent, current, future):
    """Assert keeping an event with start and end times relative to the
    flapping windows."""
    status = EventFlappingStatus.keep
    assert_event_status(status, event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_past_event_retire(iso_dates):
    """Test that an event ending before should be retired."""
    event_start, event_end, recent, current, future = tuple(iso_dates)
    assert_event_retire(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_recent_event_keep(iso_dates):
    """Test that an event ending during the recent to current flapping window
    should be kept."""
    event_start, recent, event_end, current, future = tuple(iso_dates)
    assert_event_keep(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_current_event_keep(iso_dates):
    """Test that an event within the recent to current flapping windows should
    be kept."""
    recent, event_start, event_end, current, future = tuple(iso_dates)
    assert_event_keep(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_ongoing_event_keep(iso_dates):
    """Test that an event starting within the recent to current flapping
    windows should be kept."""
    recent, event_start, current, event_end, future = tuple(iso_dates)
    assert_event_keep(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_surrounding_event_keep(iso_dates):
    """Test that an event surrounding the recent to current flapping windows
    should be kept."""
    event_start, recent, current, event_end, future = tuple(iso_dates)
    assert_event_keep(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_planned_event_delete(iso_dates):
    """Test that an event planned between the flapping windows should be deleted."""
    recent, current, event_start, event_end, future = tuple(iso_dates)
    assert_event_delete(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_future_event_keep(iso_dates):
    """Test that a future event ending after the future time should be kept."""
    recent, current, event_start, future, event_end = tuple(iso_dates)
    assert_event_keep(event_start, event_end, recent, current, future)

@given(iso_dates = iso_date_lists)
def test_far_future_event_keep(iso_dates):
    """Test that a future event starting after the future time should be kept."""
    recent, current, future, event_start, event_end = tuple(iso_dates)
    assert_event_keep(event_start, event_end, recent, current, future)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

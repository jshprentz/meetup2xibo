"""Test event comparison and reporting."""

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

MINIMUM_TEST_DATE = datetime(2019, 1, 1, 0, 0, 0)
MAXIMUM_TEST_DATE = datetime(2029, 12, 31, 23, 59, 59)

def iso_format(the_date_time):
    """Format a date/time in ISO YYYY-MM-DD hh:mm:ss format."""
    return the_date_time.strftime('%Y-%m-%d %H:%M:%S')

typical_dates = st.datetimes(min_value = MINIMUM_TEST_DATE, max_value = MAXIMUM_TEST_DATE)
iso_dates = typical_dates.map(iso_format)

#@pytest.fixture
#def crud_lister():
#    """Return an event CRUD log line lister."""
#    return CrudLister()


def make_event(
        name=SAMPLE_NAME,
        location=SAMPLE_LOCATION,
        start_time=SAMPLE_START_TIME,
        end_time=SAMPLE_END_TIME,
        meetup_id=SAMPLE_MEETUP_ID):
    """Make an event with default sample values."""
    return Event(name, start_time, end_time, meetup_id, location)


def test_url():
    """Test generating a URL from an event."""
    event = make_event()
    assert event.url == "https://www.meetup.com/NOVA-Makers/events/qlpqsqyzhbqb/"

def test_equals_identical():
    """Test comparing an event with it self."""
    event = make_event()
    assert event == event

def test_equals_same():
    """Test comparing events with the same value."""
    event1 = make_event()
    event2 = make_event()
    assert event1 == event2

def test_equals_different_names():
    """Test comparing events with different names."""
    event1 = make_event()
    event2 = make_event(name="foo")
    assert event1 != event2

def test_equals_different_locations():
    """Test comparing events with different locations."""
    event1 = make_event()
    event2 = make_event(location="foo")
    assert event1 != event2

def test_equals_different_start_times():
    """Test comparing events with different start_times."""
    event1 = make_event()
    event2 = make_event(start_time="2019-05-12 10:00:00")
    assert event1 != event2

def test_equals_different_end_times():
    """Test comparing events with different end_times."""
    event1 = make_event()
    event2 = make_event(end_time="2019-05-12 19:00:00")
    assert event1 != event2

def test_equals_different_meetup_ids():
    """Test comparing events with different meetup IDs."""
    event1 = make_event()
    event2 = make_event(meetup_id="zvbxrpl")
    assert event1 != event2

def test_differences_different_names():
    """Test listing differences for events with different names."""
    event1 = make_event()
    event2 = make_event(name="foo")
    assert [('name', 'Arduino User Group', 'foo')] == event1.differences(event2)

def test_differences_different_locations():
    """Test listing differences for events with different locations."""
    event1 = make_event()
    event2 = make_event(location="foo")
    assert [('location', 'Conference Room 3', 'foo')] == event1.differences(event2)

def test_differences_different_start_times():
    """Test listing differences for events with different start_times."""
    event1 = make_event()
    event2 = make_event(start_time="2019-05-12 10:00:00")
    assert [('start time', '2019-05-12 15:00:00', '2019-05-12 10:00:00')] == event1.differences(event2)

def test_differences_different_end_times():
    """Test listing differences for events with different end_times."""
    event1 = make_event()
    event2 = make_event(end_time="2019-05-12 19:00:00")
    assert [('end time', '2019-05-12 17:00:00', '2019-05-12 19:00:00')] == event1.differences(event2)

def test_differences_different_meetup_ids():
    """Test listing differences for events with different meetup IDs."""
    event1 = make_event()
    event2 = make_event(meetup_id="zvbxrpl")
    assert [('Meetup ID', 'qlpqsqyzhbqb', 'zvbxrpl')] == event1.differences(event2)

def test_differences_multiple():
    """Test listing differences for events with multiple changes."""
    event1 = make_event()
    event2 = make_event(location="foo", start_time="2019-05-12 10:00:00")
    expected_differences = [
            ('location', 'Conference Room 3', 'foo'),
            ('start time', '2019-05-12 15:00:00', '2019-05-12 10:00:00')
            ]
    assert expected_differences == event1.differences(event2)

def test_equals_non_event():
    """Test comparing an event with a non-event."""
    event = make_event()
    assert event != "foo"

def test_hash_identical():
    """Test that an event hash is always the same."""
    event = make_event()
    assert hash(event) == hash(event)

def test_hash_same():
    """Test that two events with the same values hash the same."""
    event1 = make_event()
    event2 = make_event()
    assert hash(event1) == hash(event2)

@given(st.text(max_size=15))
def test_hash_different_names(other_name):
    """Test hashing events with different names."""
    assume(other_name != SAMPLE_NAME)
    event1 = make_event()
    event2 = make_event(name=other_name)
    assert hash(event1) != hash(event2)

@given(st.text(max_size=15))
def test_hash_different_locations(other_location):
    """Test hashing events with different locations."""
    assume(other_location != SAMPLE_LOCATION)
    event1 = make_event()
    event2 = make_event(location=other_location)
    assert hash(event1) != hash(event2)

@given(iso_dates)
def test_hash_different_start_times(other_start_time):
    """Test hashing events with different start_times."""
    assume(other_start_time != SAMPLE_START_TIME)
    event1 = make_event()
    event2 = make_event(start_time=other_start_time)
    assert hash(event1) != hash(event2)

@given(iso_dates)
def test_hash_different_end_times(other_end_time):
    """Test hashing events with different end_times."""
    assume(other_end_time != SAMPLE_END_TIME)
    event1 = make_event()
    event2 = make_event(end_time=other_end_time)
    assert hash(event1) != hash(event2)

@given(st.text(min_size=8, max_size=10))
def test_hash_different_meetup_ids(other_meetup_id):
    """Test hashing events with different meetup IDs."""
    assume(other_meetup_id != SAMPLE_MEETUP_ID)
    event1 = make_event()
    event2 = make_event(meetup_id=other_meetup_id)
    assert hash(event1) != hash(event2)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

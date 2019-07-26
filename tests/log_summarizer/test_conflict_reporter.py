"""Test the conflict reporter."""

from meetup2xibo.log_summarizer.conflict import Conflict
from meetup2xibo.log_summarizer.event import Event
from meetup2xibo.log_summarizer.conflict_reporter import ConflictReporter
import pytest
from hypothesis import given, assume, example
import hypothesis.strategies as st

SAMPLE_MEETUP_ID = 'qlpqsqyzhbqb'
SAMPLE_NAME = 'Arduino User Group'
SAMPLE_LOCATION = 'Conference Room 3'
SAMPLE_START_TIME = '2019-05-12 15:00:00'
SAMPLE_END_TIME = '2019-05-12 17:00:00'

SAMPLE_OTHER_MEETUP_ID = '75636384'
SAMPLE_OTHER_NAME = 'Tech Toastmasters'
SAMPLE_OTHER_START_TIME = '2019-05-13 18:00:00'
SAMPLE_OTHER_END_TIME = '2019-05-13 20:00:00'

place_names = st.text(min_size=1, max_size=15)
place_name_lists = (st.lists(place_names, min_size=2, max_size=4))


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


@pytest.fixture
def conflict_reporter():
    """Return a conflict reporter."""
    return ConflictReporter()

@given(place_name=place_names)
def test_add_checked_place_one(place_name, conflict_reporter):
    """Test adding and sorting one place name."""
    conflict_reporter.clear()
    conflict_reporter.add_checked_place(place_name)
    sorted_places = conflict_reporter.sorted_checked_places()
    assert [place_name] == sorted_places

@given(place_name_list = place_name_lists)
def test_add_checked_place_sorted(place_name_list, conflict_reporter):
    """Test adding and sorting a list of place names."""
    conflict_reporter.clear()
    for place_name in place_name_list:
        conflict_reporter.add_checked_place(place_name)
    sorted_places = conflict_reporter.sorted_checked_places()
    assert len(place_name_list) == len(sorted_places)
    for place_name in place_name_list:
        assert place_name in sorted_places
    for i in range(0, len(sorted_places) - 1):
        assert sorted_places[i] <= sorted_places[i + 1]

def test_add_conflict_one(conflict_reporter):
    """Test adding and sorting one conflict."""
    conflict = make_conflict()
    conflict_reporter.add_conflict("Woodshop", conflict)
    sorted_conflict_places = conflict_reporter.sorted_conflict_places()
    assert sorted_conflict_places == [("Woodshop", [conflict])]

def test_add_conflict_one_place_two_events(conflict_reporter):
    """Test adding and sorting two conflicts at the same place."""
    conflict1 = make_conflict()
    conflict2 = make_conflict(start_time=SAMPLE_OTHER_START_TIME, end_time=SAMPLE_OTHER_END_TIME)
    conflict_reporter.add_conflict("Woodshop", conflict1)
    conflict_reporter.add_conflict("Woodshop", conflict2)
    sorted_conflict_places = conflict_reporter.sorted_conflict_places()
    assert sorted_conflict_places == [("Woodshop", [conflict1, conflict2])]

def test_add_conflict_two_places_one_event(conflict_reporter):
    """Test adding and sorting two conflicts at different places."""
    conflict1 = make_conflict()
    conflict2 = make_conflict(start_time=SAMPLE_OTHER_START_TIME, end_time=SAMPLE_OTHER_END_TIME)
    conflict_reporter.add_conflict("Woodshop", conflict1)
    conflict_reporter.add_conflict("Metal Shop", conflict2)
    sorted_conflict_places = conflict_reporter.sorted_conflict_places()
    assert sorted_conflict_places == [("Metal Shop", [conflict2]), ("Woodshop", [conflict1])]

def test_has_conflicts(conflict_reporter):
    """Test adding and testing for a conflict."""
    conflict = make_conflict()
    conflict_reporter.add_conflict("Woodshop", conflict)
    assert conflict_reporter.has_conflicts()

def test_clear(conflict_reporter):
    """Test clearing conflicts and places."""
    conflict = make_conflict()
    conflict_reporter.add_checked_place("Metal Shop")
    conflict_reporter.add_conflict("Woodshop", conflict)
    conflict_reporter.clear()
    assert not conflict_reporter.has_conflicts()
    assert conflict_reporter.sorted_conflict_places() == []
    assert conflict_reporter.sorted_checked_places() == []


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

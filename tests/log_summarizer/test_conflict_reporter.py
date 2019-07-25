"""Test the conflict reporter."""

from meetup2xibo.log_summarizer.conflict_reporter import ConflictReporter
import pytest
from hypothesis import given, assume, example
import hypothesis.strategies as st

place_names = st.text(min_size=1, max_size=15)
place_name_lists = (st.lists(place_names, min_size=2, max_size=4))


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


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

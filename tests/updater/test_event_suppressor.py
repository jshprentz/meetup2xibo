"""Test the event suppressor."""

from meetup2xibo.updater.event_suppressor import EventSuppressor
from hypothesis import given, assume, example
import hypothesis.strategies as st
import pytest

meetup_ids=st.text(alphabet="abcd", min_size=3, max_size=3)

other_meetup_ids=st.text(alphabet="wxyz", min_size=3, max_size=3)

meetup_id_lists=st.lists(meetup_ids, min_size=1, max_size=4, unique=True)

@given(meetup_ids)
def test_should_suppress_empty_list(meetup_id):
    """Test that no Meetup ID is suppressed when the suppress list is empty."""
    suppressor = EventSuppressor([])
    assert not suppressor.should_suppress(meetup_id)

@given(other_meetup_ids, meetup_id_lists)
def test_should_suppress_not_in_list(meetup_id, meetup_ids_to_suppress):
    """Test that a Meetup ID is not suppressed when it is not in the suppress
    list."""
    suppressor = EventSuppressor(meetup_ids_to_suppress)
    assert not suppressor.should_suppress(meetup_id)

@given(meetup_id_lists)
def test_should_suppress_in_list(meetup_ids_to_suppress):
    """Test that a Meetup ID is suppressed when it is in the suppress list."""
    meetup_id = meetup_ids_to_suppress[0]
    suppressor = EventSuppressor(meetup_ids_to_suppress)
    assert suppressor.should_suppress(meetup_id)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

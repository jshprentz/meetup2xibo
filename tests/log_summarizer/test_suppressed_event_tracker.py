from meetup2xibo.log_summarizer.suppressed_event_tracker import SuppressedEventTracker
import pytest
from hypothesis import given, assume, example
import hypothesis.strategies as st

meetup_ids=st.text(alphabet="abcdef", min_size=1, max_size=1)

meetup_id_lists=st.lists(meetup_ids, min_size=0, max_size=4)
non_empty_meetup_id_lists=st.lists(meetup_ids, min_size=1, max_size=4)

@given(meetup_id_lists, meetup_id_lists)
def test_unneeded_ids(suppressed_ids, unchecked_ids):
    """Test reporting unneeded Meetup IDs from lists of suppressed and unchecked
    Meetup IDs."""
    tracker = SuppressedEventTracker()
    for suppressed_id in suppressed_ids:
        tracker.suppressed_id(suppressed_id)
    for unchecked_id in unchecked_ids:
        tracker.unchecked_id(unchecked_id)
    unneeded_ids = tracker.unneeded_ids()
    for unneeded_id in unneeded_ids:
        assert unneeded_id in unchecked_ids
        assert unneeded_id not in suppressed_ids

@given(non_empty_meetup_id_lists)
def test_unneeded_ids_all(unchecked_ids):
    """Test reporting all unchecked IDs when no Meetup IDs are suppressed."""
    tracker = SuppressedEventTracker()
    for unchecked_id in unchecked_ids:
        tracker.unchecked_id(unchecked_id)
    unneeded_ids = tracker.unneeded_ids()
    for unneeded_id in unneeded_ids:
        assert unneeded_id in unchecked_ids
    for unchecked_id in unchecked_ids:
        assert unchecked_id in unneeded_ids

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

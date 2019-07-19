"""Test checked and unchecked plases."""

from meetup2xibo.updater.places import CheckedPlace, UncheckedPlace
import pytest
import logging


@pytest.fixture
def woodshop():
    """Return place named woodshop."""
    return CheckedPlace("Woodshop")

@pytest.fixture
def metalshop():
    """Return place named metal shop."""
    return CheckedPlace("Metal Shop")

@pytest.fixture
def shops(woodshop, metalshop):
    """Return place named shops that contains the wood and metal shops."""
    shops = CheckedPlace("Shops")
    shops.contain(woodshop)
    shops.contain(metalshop)
    return shops


def test_contains_not(woodshop, metalshop):
    """Test not containing a place."""
    assert not woodshop.contains(metalshop)

def test_contains(shops, woodshop):
    """Test adding a contained place."""
    assert shops.contains(woodshop)
    assert not woodshop.contains(shops)

def test_no_events(woodshop, caplog):
    """Test logging nothing when there are no events."""
    caplog.set_level(logging.INFO)
    woodshop.log_conflicts("0000-00-00 00:00:00")
    assert caplog.text == ""

def test_non_overlapping_events(sample_events, woodshop, caplog):
    """Test logging nothing when events do not overlap."""
    caplog.set_level(logging.INFO)
    event1, event2 = sample_events.make_non_overlapping_events()
    woodshop.start_event(event1)
    woodshop.log_conflicts(event1.start_time)
    woodshop.end_event(event1)
    woodshop.log_conflicts(event1.end_time)
    woodshop.start_event(event2)
    woodshop.log_conflicts(event2.start_time)
    woodshop.end_event(event2)
    woodshop.log_conflicts(event2.end_time)
    assert caplog.text == ""

def test_consecutive_events(sample_events, woodshop, caplog):
    """Test logging nothing when one event follows another."""
    caplog.set_level(logging.INFO)
    event1, event2 = sample_events.make_consecutive_events()
    woodshop.start_event(event1)
    woodshop.log_conflicts(event1.start_time)
    woodshop.start_event(event2)
    woodshop.end_event(event1)
    woodshop.log_conflicts(event1.end_time)
    woodshop.end_event(event2)
    woodshop.log_conflicts(event2.end_time)
    assert caplog.text == ""

def test_overlapping_events(sample_events, woodshop, caplog):
    """Test logging when events overlap."""
    caplog.set_level(logging.INFO)
    event1, event2 = sample_events.make_overlapping_events()
    woodshop.start_event(event1)
    woodshop.log_conflicts(event1.start_time)
    woodshop.start_event(event2)
    woodshop.log_conflicts(event2.start_time)
    woodshop.end_event(event1)
    woodshop.log_conflicts(event1.end_time)
    woodshop.end_event(event2)
    woodshop.log_conflicts(event2.end_time)
    assert len(caplog.messages) == 1
    message = caplog.messages[0]
    assert "Schedule conflict: place='Woodshop'" in message
    expected_conflict_times = "Conflict(start_time='{}', end_time='{}',".format(
            event2.start_time, event1.end_time)
    assert expected_conflict_times in message
    assert event1.meetup_id in message
    assert event2.meetup_id in message

def test_straddling_events(sample_events, woodshop, caplog):
    """Test logging when one event straddles another."""
    caplog.set_level(logging.INFO)
    event1, event2 = sample_events.make_straddling_events()
    woodshop.start_event(event1)
    woodshop.log_conflicts(event1.start_time)
    woodshop.start_event(event2)
    woodshop.log_conflicts(event2.start_time)
    woodshop.end_event(event2)
    woodshop.log_conflicts(event2.end_time)
    woodshop.end_event(event1)
    woodshop.log_conflicts(event1.end_time)
    assert len(caplog.messages) == 1
    message = caplog.messages[0]
    assert "Schedule conflict: place='Woodshop'" in message
    expected_conflict_times = "Conflict(start_time='{}', end_time='{}',".format(
            event2.start_time, event2.end_time)
    assert expected_conflict_times in message
    assert event1.meetup_id in message
    assert event2.meetup_id in message

def test_same_start_events(sample_events, woodshop, caplog):
    """Test logging when events start at the same time."""
    caplog.set_level(logging.INFO)
    event1, event2 = sample_events.make_same_start_events()
    woodshop.start_event(event1)
    woodshop.start_event(event2)
    woodshop.log_conflicts(event2.start_time)
    woodshop.end_event(event1)
    woodshop.log_conflicts(event1.end_time)
    woodshop.end_event(event2)
    woodshop.log_conflicts(event2.end_time)
    assert len(caplog.messages) == 1
    message = caplog.messages[0]
    assert "Schedule conflict: place='Woodshop'" in message
    expected_conflict_times = "Conflict(start_time='{}', end_time='{}',".format(
            event1.start_time, event1.end_time)
    assert expected_conflict_times in message
    assert event1.meetup_id in message
    assert event2.meetup_id in message

def test_same_end_events(sample_events, woodshop, caplog):
    """Test logging when events end at the same time."""
    caplog.set_level(logging.INFO)
    event1, event2 = sample_events.make_same_end_events()
    woodshop.start_event(event1)
    woodshop.log_conflicts(event1.start_time)
    woodshop.start_event(event2)
    woodshop.log_conflicts(event2.start_time)
    woodshop.end_event(event1)
    woodshop.end_event(event2)
    woodshop.log_conflicts(event2.end_time)
    assert len(caplog.messages) == 1
    message = caplog.messages[0]
    assert "Schedule conflict: place='Woodshop'" in message
    expected_conflict_times = "Conflict(start_time='{}', end_time='{}',".format(
            event2.start_time, event2.end_time)
    assert expected_conflict_times in message
    assert event1.meetup_id in message
    assert event2.meetup_id in message

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

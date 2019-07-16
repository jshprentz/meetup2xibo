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
    woodshop.log_conflicts()
    assert caplog.text == ""

def test_non_overlapping_events(sample_events, woodshop, caplog):
    """Test logging nothing when events do not overlap."""
    caplog.set_level(logging.INFO)
    event1, event2 = sample_events.make_non_overlapping_events()
    woodshop.start_event(event1)
    woodshop.end_event(event1)
    woodshop.start_event(event2)
    woodshop.end_event(event2)
    woodshop.log_conflicts()
    assert caplog.text == ""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

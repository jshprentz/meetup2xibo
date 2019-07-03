"""Test checked and unchecked plases."""

from meetup2xibo.updater.places import CheckedPlace, UncheckedPlace
import pytest


def test_contains_not():
    """Test not containing a place."""
    place = CheckedPlace("Woodshop")
    other_place = CheckedPlace("Classroom")
    assert not place.contains(other_place)

def test_contains():
    """Test adding a contained place."""
    place = CheckedPlace("Woodshop")
    other_place = CheckedPlace("Classroom")
    place.contain(other_place)
    assert place.contains(other_place)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

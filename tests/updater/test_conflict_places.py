"""Test adding places and containment to conflict places."""

from meetup2xibo.updater.conflict_places import ConflictPlaces
from meetup2xibo.updater.places import CheckedPlace, UncheckedPlace
import pytest


@pytest.fixture
def conflict_places():
    """Return a conflict places."""
    return ConflictPlaces()

def assert_conflict_place(conflict_places, name, expected_class):
    """Assert that the named conflict place has the expected class."""
    place = conflict_places.named_place(name)
    assert isinstance(place, expected_class)
    assert place.name == name

def assert_contains(conflict_places, name, other_names):
    """Assert that the named place contains places with the other names."""
    place = conflict_places.named_place(name)
    for other_name in other_names:
        other_place = conflict_places.named_place(other_name)
        assert place.contains(other_place)

def test_emtpy_conflict_places(conflict_places):
    """Test getting a place from an empty conflict places."""
    assert conflict_places.named_place("Woodshop") == None

def test_add_checked_place(conflict_places):
    """Test adding a checked place."""
    conflict_places.add_checked_place("Woodshop")
    assert_conflict_place(conflict_places, "Woodshop", CheckedPlace)

def test_add_containing_place_new(conflict_places):
    """Test adding a new place containing other places."""
    new_place = "Metal Shop"
    contained_places = ["Room A", "Room B"]
    conflict_places.add_containing_place(new_place, contained_places)
    assert_conflict_place(conflict_places, new_place, UncheckedPlace)
    for name in contained_places:
        assert_conflict_place(conflict_places, name, UncheckedPlace)
    assert_contains(conflict_places, new_place, contained_places)
    
def test_add_containing_place_mixed(conflict_places):
    """Test adding a known place containing known and unknown places."""
    known_place = "Metal Shop"
    conflict_places.add_checked_place(known_place)
    contained_places = ["Room A", "Room B"]
    conflict_places.add_checked_place("Room B")
    conflict_places.add_containing_place(known_place, contained_places)
    assert_conflict_place(conflict_places, known_place, CheckedPlace)
    assert_conflict_place(conflict_places, "Room A", UncheckedPlace)
    assert_conflict_place(conflict_places, "Room B", CheckedPlace)
    assert_contains(conflict_places, known_place, contained_places)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

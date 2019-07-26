"""Test adding places and containment to conflict places."""

from meetup2xibo.updater.conflict_places import ConflictPlaces, ConflictPlacesLoader
from meetup2xibo.updater.places import CheckedPlace, UncheckedPlace
import pytest

CHECKED_PLACE_NAMES = ["Woodshop", "Classroom", "CAD Lab"]

UNCHECKED_PLACE_NAMES = ["Shops", "Metal Shop", "Computer Room", "Printer Room"]

CONTAINING_PLACES = [
    {"place": "Shops", "contains": ["Woodshop", "Metal Shop"]},
    {"place": "CAD Lab", "contains": ["Computer Room", "Printer Room"]}
    ]

@pytest.fixture
def conflict_places():
    """Return a conflict places."""
    return ConflictPlaces()

@pytest.fixture
def conflict_places_loader(conflict_places):
    """Return a conflict places loader."""
    return ConflictPlacesLoader(conflict_places, CHECKED_PLACE_NAMES,
            CONTAINING_PLACES)

def assert_conflict_place(conflict_places, name, expected_class):
    """Assert that the named conflict place has the expected class."""
    place = conflict_places.named_place(name)
    assert isinstance(place, expected_class)
    assert place.name == name

def assert_checked_places(conflict_places):
    """Assert that the usual places are checked places."""
    for name in CHECKED_PLACE_NAMES:
        assert_conflict_place(conflict_places, name, CheckedPlace)

def assert_unchecked_places(conflict_places):
    """Assert that the usual places are unchecked places."""
    for name in UNCHECKED_PLACE_NAMES:
        assert_conflict_place(conflict_places, name, UncheckedPlace)

def assert_contains(conflict_places, name, other_names):
    """Assert that the named place contains places with the other names."""
    place = conflict_places.named_place(name)
    for other_name in other_names:
        other_place = conflict_places.named_place(other_name)
        assert place.contains(other_place)

def assert_containing_places(conflict_places):
    """Assert that conflict places knows the containing places."""
    for place in CONTAINING_PLACES:
        assert_contains(conflict_places, place["place"], place["contains"])

def test_add_checked_places(conflict_places, conflict_places_loader):
    """Test adding checked places."""
    conflict_places_loader.add_checked_places()
    assert_checked_places(conflict_places)

def test_add_containing_places(conflict_places, conflict_places_loader):
    """Test adding contained places."""
    conflict_places_loader.add_containing_places()
    assert_containing_places(conflict_places)

def test_load(conflict_places, conflict_places_loader):
    """Test loading checked and containing places into conflict places."""
    loaded_conflict_places = conflict_places_loader.load()
    assert_checked_places(loaded_conflict_places)
    assert_unchecked_places(loaded_conflict_places)
    assert_containing_places(loaded_conflict_places)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

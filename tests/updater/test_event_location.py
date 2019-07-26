"""Test event locations."""


from meetup2xibo.updater.event_location import EventLocation
import pytest

SAMPLE_PLACES = ["Woodshop", "Classroom A"]
OTHER_PLACES = ["Conference Room 1"]


def test_repr():
    """Test that repr returns repr(description string)."""
    location = EventLocation("test", SAMPLE_PLACES)
    assert repr(location) == "EventLocation('test', ['Woodshop', 'Classroom A'])"

def test_str():
    """Test that str returns str(description string)."""
    location = EventLocation("test", SAMPLE_PLACES)
    assert str(location) == str("test")

def test_equals_same():
    """Test that two identical locations are equals."""
    location1 = EventLocation("test", SAMPLE_PLACES)
    location2 = EventLocation("test", SAMPLE_PLACES)
    assert location1 == location2

def test_equals_different_descriptions():
    """Test that two different locations are not equals."""
    location1 = EventLocation("test1", SAMPLE_PLACES)
    location2 = EventLocation("test2", SAMPLE_PLACES)
    assert location1 != location2

def test_equals_different_places():
    """Test that two different locations are not equals."""
    location1 = EventLocation("test", SAMPLE_PLACES)
    location2 = EventLocation("test", OTHER_PLACES)
    assert location1 != location2

def test_bool_true():
    """Test that bool returns true for a non-empty string."""
    location = EventLocation("test", SAMPLE_PLACES)
    assert location

def test_bool_false():
    """Test that bool returns false for an empty string."""
    location = EventLocation("", SAMPLE_PLACES)
    assert not location

test_place_lists = [
    ([], ""),
    (["abc"], "abc"),
    (["def", "abc"], "def and abc"),
    (["def", "abc", "ghi"], "def, abc, and ghi"),
    (["def", "jkl", "abc", "ghi"], "def, jkl, abc, and ghi"),
]

@pytest.mark.parametrize("place_list,expected_phrase", test_place_lists)
def test_format_place_list(place_list, expected_phrase):
    """Test formatting place lists as a phrase retaining order."""
    phrase = EventLocation.format_place_list(place_list)
    assert expected_phrase == phrase

@pytest.mark.parametrize("place_list,expected_phrase", test_place_lists)
def test_from_places(place_list, expected_phrase):
    """Test making an event location from a list of places."""
    event_location = EventLocation.from_places(place_list)
    assert event_location.description == expected_phrase
    assert event_location.places == place_list

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

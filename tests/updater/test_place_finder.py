"""Test finding places from a Meetup event."""

from meetup2xibo.updater.event_converter import PartialEvent
from meetup2xibo.updater.place_finder import PlaceFinder
from meetup2xibo.updater.phrase_mapper import PhraseMapper
from ahocorasick import Automaton
import pytest


LOCATION_PHRASES = [
    ("Classroom A and B", "Classroom A/B"),
    ("Classroom A/B", "Classroom A/B"),
    ("Classroom A", "Classroom A"),
    ("Conference Rm 1", "Conference Room 1"),
    ("Conference Rm 2", "Conference Room 2"),
    ("Metal shop", "Metal Shop"),
    ("Metalshop", "Metal Shop"),
]

DEFAULT_PHRASES = [
    ("Nova Labs", "Nova Labs"),
    ("TBD", "TBD")
]

TEST_VENUE_MAPPINGS_1= [
    ("","[]",[]),
    ("TBD","[]",[]),
    ("*Nova Labs (Classroom A)","[ ]",["Classroom A"]),
    ("*Nova Labs (Classroom A  and B)","[]",["Classroom A/B"]),
    ("*Nova Labs (Classroom A and B)","[Metal shop]",["Classroom A/B", "Metal Shop"]),
    ("Nova Labs","[Metal shop]",["Metal Shop"]),
    ("Nova Labs","",[]),
    ("Nova  Labs","See http://nova-labs.org/contact/#parking for map and parking details.",[]),
]

TEST_VENUE_MAPPINGS_2 = [
    ("","[]",[]),
    ("TBD","[]",["TBD"]),
    ("*Nova Labs (Classroom A)","[ ]",["Classroom A"]),
    ("*Nova Labs (Classroom A  and B)","[]",["Classroom A/B"]),
    ("*Nova Labs (Classroom A and B)","[Metal shop]",["Classroom A/B", "Metal Shop"]),
    ("Nova Labs","[Metal shop]",["Metal Shop"]),
    ("Nova  Labs","",["Nova Labs"]),
    ("Nova  Labs","See http://nova-labs.org/contact/#parking for map and parking details.",["Nova Labs"]),
]

TEST_FIND_LOCATIONS = [
    ("", "[]",[]),
    ("*Nova Labs (Classroom A)", "[ ]",["Classroom A"]),
    ("Nova Labs (Classroom A)", "[Classroom A]", ["Classroom A"]),
    ("*Nova Labs (Classroom A  and B)", "[]",["Classroom A/B"]),
    ("*Nova Labs (Classroom A and B)", "[Metal shop]",["Classroom A/B", "Metal Shop"]),
    ("*Nova Labs (Conference Rm 1)", "Conference Rm 2 and Conference Rm 1", ["Conference Room 1", "Conference Room 2"]),
    ("Nova Labs", "[Metal shop]",["Metal Shop"]),
    ("Nova Labs", "[Metalshop]",["Metal Shop"]),
    ("Nova Labs", "See http://nova-labs.org/contact/#parking for map and parking details.",["Nova Labs"]),
    ("NVCC Seefeldt Building", "Seefeldt Building room #228", []),
]

def make_partial_event(venue_name = "", find_us = "", name = "Some Event"):
    """Return a partial event with some test values."""
    return PartialEvent("A12", name, "2019-03-01 19:00:00",
        "2019-03-01 21:00:00", venue_name, find_us)

@pytest.fixture(scope="module")
def location_phrase_mapper():
    """Return a phrase mapper initialized with the location phrases."""
    return PhraseMapper(Automaton(), LOCATION_PHRASES).setup()

@pytest.fixture(scope="module")
def default_phrase_mapper():
    """Return a phrase mapper initialized with the default phrases."""
    return PhraseMapper(Automaton(), DEFAULT_PHRASES).setup()

@pytest.fixture(scope="module")
def phrase_mappers(location_phrase_mapper, default_phrase_mapper):
    """Return a list of phrase mappers."""
    return [location_phrase_mapper, default_phrase_mapper]

@pytest.fixture
def place_finder(phrase_mappers):
    """Return a place finder with the test phrase mappers."""
    return PlaceFinder(phrase_mappers)

@pytest.mark.parametrize("venue_name,find_us,expected_places", TEST_VENUE_MAPPINGS_1)
def test_map_phrases_in_venue(venue_name, find_us, expected_places, location_phrase_mapper):
    """Test mapping phrases in venue and find us fields."""
    partial_event = make_partial_event(venue_name = venue_name, find_us = find_us)
    places = PlaceFinder.map_phrases_in_venue(location_phrase_mapper, partial_event)
    assert places == expected_places

@pytest.mark.parametrize("venue_name,find_us,expected_places", TEST_VENUE_MAPPINGS_2)
def test_map_from_phrase_mappers(venue_name, find_us, expected_places, place_finder):
    """Test mapping phrases using all phrase mappers."""
    partial_event = make_partial_event(venue_name = venue_name, find_us = find_us)
    places = place_finder.map_from_phrase_mappers(partial_event)
    assert places == expected_places

@pytest.mark.parametrize("venue_name,find_us,expected_place_list", TEST_FIND_LOCATIONS)
def test_find_places(venue_name, find_us, expected_place_list, place_finder):
    """Test finding places from an event's venue name and "how to find us"
    information."""
    partial_event = make_partial_event(venue_name = venue_name, find_us = find_us)
    place_list = place_finder.find_places(partial_event)
    assert expected_place_list == place_list


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Test building locations from a Meetup event."""

from meetup2xibo.updater.event_converter import PartialEvent
from meetup2xibo.updater.location_builder import LocationBuilder
from meetup2xibo.updater.phrase_mapper import PhraseMapper
from ahocorasick import Automaton
import pytest


LOCATION_PHRASES = [
    ("Classroom A and B", "Classroom A/B"),
    ("Classroom A/B", "Classroom A/B"),
    ("Classroom A", "Classroom A"),
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

TEST_EVENT_LOCATIONS = [
    ("","[]",""),
    ("*Nova Labs (Classroom A)","[ ]","Classroom A"),
    ("*Nova Labs (Classroom A  and B)","[]","Classroom A/B"),
    ("*Nova Labs (Classroom A and B)","[Metal shop]","Classroom A/B and Metal Shop"),
    ("Nova Labs","[Metal shop]","Metal Shop"),
    ("Nova Labs","[Metalshop]","Metal Shop"),
    ("Nova Labs","See http://nova-labs.org/contact/#parking for map and parking details.","Nova Labs"),
    ("NVCC Seefeldt Building", "Seefeldt Building room #228", ""),
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
def location_builder(phrase_mappers):
    """Return a location builder with the test phrase mappers."""
    return LocationBuilder(phrase_mappers)

@pytest.mark.parametrize("venue_name,find_us,expected_locations", TEST_VENUE_MAPPINGS_1)
def test_map_phrases_in_venue(venue_name, find_us, expected_locations, location_phrase_mapper):
    """Test mapping phrases in venue and find us fields."""
    partial_event = make_partial_event(venue_name = venue_name, find_us = find_us)
    locations = LocationBuilder.map_phrases_in_venue(location_phrase_mapper, partial_event)
    assert locations == expected_locations

@pytest.mark.parametrize("venue_name,find_us,expected_locations", TEST_VENUE_MAPPINGS_2)
def test_map_from_phrase_mappers(venue_name, find_us, expected_locations, location_builder):
    """Test mapping phrases using all phrase mappers."""
    partial_event = make_partial_event(venue_name = venue_name, find_us = find_us)
    locations = location_builder.map_from_phrase_mappers(partial_event)
    assert locations == expected_locations

@pytest.mark.parametrize("venue_name,find_us,expected_location", TEST_EVENT_LOCATIONS)
def test_build_location(venue_name, find_us, expected_location, location_builder):
    """Test building a location from an event's venue name and "how to
    find us" information."""
    partial_event = make_partial_event(venue_name = venue_name, find_us = find_us)
    location = location_builder.build_location(partial_event)
    assert expected_location == location

test_location_lists = [
    (["abc"], "abc"),
    (["def", "abc"], "def and abc"),
    (["def", "abc", "ghi"], "def, abc, and ghi"),
    (["def", "jkl", "abc", "ghi"], "def, jkl, abc, and ghi"),
]

@pytest.mark.parametrize("location_list,expected_phrase", test_location_lists)
def test_format_location_list(location_list, expected_phrase):
    """Test formatting location lists as a phrase retaining order."""
    phrase = LocationBuilder.format_location_list(location_list)
    assert expected_phrase == phrase




# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

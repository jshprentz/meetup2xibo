"""Test extracting locations from a Meetup event."""

from .context import meetup2xibo
from meetup2xibo.location_extractor import LocationExtractor
import pytest


test_event_locations = [
    ("","[]","TBD"),
    ("*Nova Labs (Classroom A)","[ ]","Classroom A"),
    ("*Nova Labs (Classroom A and B)","[]","Classroom A/B"),
    ("*Nova Labs (Classroom B)","[]","Classroom B"),
    ("*Nova Labs (Classroom B)","[Woodshop]","Classroom B and Woodshop"),
    (" Nova Labs: Computer Lab","[ ]","Computer Lab"),
    ("*Nova Labs (Conference Rm 1)","[ ]","Conference Room 1"),
    ("*Nova Labs (Conference Rm 1)","Conference rm 1","Conference Room 1"),
    ("*Nova Labs (Conference Rm 1)","[Metal shop]","Conference Room 1 and Metal Shop"),
    ("*Nova Labs (Conference Rm 2)","[ ]","Conference Room 2"),
    ("*Nova Labs (Conference Rm 3)","[Conference rm  (30min) and woodshop]","Conference Room 3 and Woodshop"),
    ("*Nova Labs (Conference Rm 3)","Conference Room 3","Conference Room 3"),
    ("Nova Labs","In the woodshop","Woodshop"),
    ("Nova Labs","[Metal shop]","Metal Shop"),
    ("Nova Labs","[Metalshop]","Metal Shop"),
    ("*Nova Labs (Orange Bay)","[]","Orange Bay"),
    ("Nova Labs","[Orange Bay and Classroom A/B]","Classroom A/B and Orange Bay"),
    ("Nova Labs","[Outback in Blacksmithing alley, behind NovaLabs ]","Blacksmithing Alley outside behind Nova Labs"),
    ("Nova Labs","Out back in the parking lot","Blacksmithing Alley outside behind Nova Labs"),
    ("Nova Labs","[outback, outside]","Blacksmithing Alley outside behind Nova Labs"),
    ("Nova Labs","See http://nova-labs.org/contact/#parking for map and parking details.","TBD"),
    ("Nova Labs","There are three entrances to Issac Newton Square. One from Sunset Hills Rd at Metro Center Dr, go through the park and ride and over the bike path. The other two are off Wiehle Ave, one has a light the other does not. [Orange Room]","Orange Bay"),
    ("Nova Labs","[woodshop]","Woodshop"),
]


#@pytest.mark.xfail(reason="Not implemented yet")
@pytest.mark.parametrize("venue_name,find_us,expected_location", test_event_locations)
def test_extract_location(venue_name, find_us, expected_location):
    """Test extracting a location from an event's venue name and "how to
    find us" information."""
    extractor = LocationExtractor.from_nova_labs()
    location = extractor.extract(venue_name, find_us)
    assert expected_location == location

test_location_lists = [
    (["abc"], "abc"),
    (["def", "abc"], "abc and def"),
    (["def", "abc", "ghi"], "abc, def, and ghi"),
    (["def", "jkl", "abc", "ghi"], "abc, def, ghi, and jkl"),
]

@pytest.mark.parametrize("location_list,expected_phrase", test_location_lists)
def test_format_location_list(location_list, expected_phrase):
    """Test formatting location lists as a phrase."""
    extractor = LocationExtractor(None)
    phrase = extractor.format_location_list(location_list)
    assert expected_phrase == phrase

@pytest.mark.parametrize("location_list,expected_phrase", test_location_lists)
def test_format_locations(location_list, expected_phrase):
    """Test formatting location sets as a phrase."""
    location_set = set(location_list)
    extractor = LocationExtractor(None)
    phrase = extractor.format_locations(location_set)
    assert expected_phrase == phrase

def test_format_locations_empty():
    """Test formatting empty location sets as a phrase."""
    location_set = set()
    extractor = LocationExtractor(None)
    phrase = extractor.format_locations(location_set)
    assert "TBD" == phrase


test_location_phrases = [
    ("Nova Labs (Classroom A and B)", ["Classroom A/B"]),
    ("[Classroom A/B]", ["Classroom A/B"]),
    ("*Nova Labs (Classroom  A)", ["Classroom A"]),
    ("First hour in Classroom A, then metal shop", ["Classroom A", "Metal Shop"]),
]

@pytest.mark.parametrize("location_text,expected_location_list", test_location_phrases)
def test_extract_from_text(location_text, expected_location_list):
    """Test extracting locations from some text."""
    expected_location_set = set(expected_location_list)
    extractor = LocationExtractor.from_nova_labs()
    location_set = extractor.extract_from_text(location_text)
    assert expected_location_set == location_set



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

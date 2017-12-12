"""Test extracting locations from a Meetup event."""

from .context import meetup2xibo
from meetup2xibo.location_extractor import LocationExtractor
import pytest


LOCATION_PHRASES = [
    ("Classroom A and B", "Classroom A/B"),
    ("Classroom A/B", "Classroom A/B"),
    ("Classroom A", "Classroom A"),
    ("Metal shop", "Metal Shop"),
    ("Metalshop", "Metal Shop"),
]

test_event_locations = [
    ("","[]","Nova Labs"),
    ("*Nova Labs (Classroom A)","[ ]","Classroom A"),
    ("*Nova Labs (Classroom A and B)","[]","Classroom A/B"),
    ("*Nova Labs (Classroom A and B)","[Metal shop]","Classroom A/B and Metal Shop"),
    ("Nova Labs","[Metal shop]","Metal Shop"),
    ("Nova Labs","[Metalshop]","Metal Shop"),
    ("Nova Labs","See http://nova-labs.org/contact/#parking for map and parking details.","Nova Labs"),
]


#@pytest.mark.xfail(reason="Not implemented yet")
@pytest.mark.parametrize("venue_name,find_us,expected_location", test_event_locations)
def test_extract_location(venue_name, find_us, expected_location):
    """Test extracting a location from an event's venue name and "how to
    find us" information."""
    extractor = LocationExtractor.from_location_phrases(LOCATION_PHRASES, "Nova Labs")
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
    extractor = LocationExtractor(None, None)
    phrase = extractor.format_location_list(location_list)
    assert expected_phrase == phrase


test_location_phrases = [
    ("Nova Labs (Classroom A and B)", ["Classroom A/B"]),
    ("[Classroom A/B]", ["Classroom A/B"]),
    ("*Nova Labs (Classroom  A)", ["Classroom A"]),
    ("First hour in Classroom A, then metal shop", ["Classroom A", "Metal Shop"]),
    ("No location here", []),
]

@pytest.mark.parametrize("location_text,expected_location_list", test_location_phrases)
def test_extract_from_text(location_text, expected_location_list):
    """Test extracting locations from some text."""
    expected_location_set = set(expected_location_list)
    extractor = LocationExtractor.from_location_phrases(LOCATION_PHRASES, "Foo")
    location_set = extractor.extract_from_text(location_text)
    assert expected_location_set == location_set



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Test the event converter from Meetup JSON to event object."""

from .context import meetup2xibo
from meetup2xibo.event_converter import EventConverter, Event
from meetup2xibo.location_extractor import LocationExtractor
from hypothesis import given, assume, example
from hypothesis.strategies import integers, text
import string
import time
import pytest


END_OF_EPOCH_SEC = (1 << 31) - 1

EXPECTED_TIMEZONES = ["EST", "EDT"]

event_prefixes = text(alphabet = string.ascii_uppercase, min_size = 2, max_size = 2)
event_names = text(min_size = 1)

JSON_EVENT_WITH_VENUE = {
    "duration": 8100000,
    "how_to_find_us": "Nova Labs is a short walk north from the Wiehle-Reston East Metro station (Silver line), and, for cyclists, the W&OD trail crosses one of the parking lot driveways.",
    "id": "bztfpmywpbbc",
    "name": "Computational Mathematics: P=NP for students and engineers at Nova Labs",
    "time": 1511223300000,
    "venue": {
        "name": "*Nova Labs (Conference Rm 2)"
    }
}

EVENT_WITH_VENUE = Event(
    meetup_id = "bztfpmywpbbc",
    name = "Computational Mathematics: P=NP for students and engineers at Nova Labs",
    start_time = "2017-11-20 19:15:00",
    end_time = "2017-11-20 21:30:00",
    location = "Conference Room 2")

JSON_EVENT_WITH_UNKNOWN_VENUE = {
    "duration": 8100000,
    "how_to_find_us": "Somewhere",
    "id": "bztfpmywpbbc",
    "name": "Computational Mathematics: P=NP for students and engineers at Nova Labs",
    "time": 1511223300000,
    "venue": {
        "name": "Somewhere else"
    }
}

EVENT_WITH_UNKNOWN_VENUE = Event(
    meetup_id = "bztfpmywpbbc",
    name = "Computational Mathematics: P=NP for students and engineers at Nova Labs",
    start_time = "2017-11-20 19:15:00",
    end_time = "2017-11-20 21:30:00",
    location = "Somewhere else - Somewhere")


JSON_EVENT_WITHOUT_VENUE = {
    "duration": 9000000,
    "how_to_find_us": "Out back in the parking lot",
    "id": "jdvswnywpbhc",
    "name": "BL: Blacksmithing for supervised practice and fun",
    "time": 1511643600000,
}

EVENT_WITHOUt_VENUE = Event(
    meetup_id = "jdvswnywpbhc",
    name = "Blacksmithing for supervised practice and fun",
    start_time = "2017-11-25 16:00:00",
    end_time = "2017-11-25 18:30:00",
    location = "Blacksmithing Alley")


COMPLETE_JSON_EVENT = {
    "created": 1509832042000,
    "description": "<p>Come out and learn the safe operation for the Enco vertical mill. We will cover the set-up of the mill, methods of securing parts, basic end mill bits, table operations, and understanding the Digital Read Out (DRO)</p> <p>Sign Off: Enco vertical mill</p> <p>Clothing: \u00a0Please do not wear synthetics. \u00a0Closed toed shoes required. \u00a0Long pants highly recommended.</p> <p>Prerequisites:\u00a0</p> <p>1. Documented Nova Labs Green Orientation class.\u00a0</p> <p>2.\u00a0Metal shop Yellow\u00a0is required to use the vertical mill independently without supervision.\u00a0You may use it on Metal Shop Mondays and with supervision while you wait for the Yellow class with this 101 class sign-off.</p> <p>**Refund is not issued if prerequisites or safety dress code is not met at the time of the class.\u00a0</p> ",
    "duration": 10800000,
    "fee": {
        "accepts": "wepay",
        "amount": 65.0,
        "currency": "USD",
        "description": "per person",
        "label": "price",
        "required": True
    },
    "group": {
        "created": 1333912341000,
        "id": 3629072,
        "join_mode": "open",
        "lat": 38.959999084472656,
        "localized_location": "Reston, VA",
        "lon": -77.33999633789062,
        "name": "NOVA Makers",
        "region": "en_US",
        "urlname": "NOVA-Makers",
        "who": "Makers"
    },
    "how_to_find_us": "[Metal Shop]",
    "id": "244824259",
    "link": "https://www.meetup.com/NOVA-Makers/events/244824259/",
    "local_date": "2017-11-21",
    "local_time": "18:30",
    "name": "MW: Enco Vertical Mill 101",
    "rsvp_limit": 4,
    "status": "upcoming",
    "time": 1511307000000,
    "updated": 1509832042000,
    "utc_offset": -18000000,
    "venue": {
        "address_1": "1916 Issac Newton Sq West",
        "city": "Reston",
        "country": "us",
        "id": 23097362,
        "lat": 38.954105377197266,
        "localized_country_name": "USA",
        "lon": -77.33885955810547,
        "name": "Nova Labs",
        "repinned": False,
        "state": "VA",
        "zip": ""
    },
    "visibility": "public",
    "waitlist_count": 0,
    "yes_rsvp_count": 4
}

COMPLETE_EVENT = Event(
    meetup_id = "244824259",
    name = "Enco Vertical Mill 101",
    start_time = "2017-11-21 18:30:00",
    end_time = "2017-11-21 21:30:00",
    location = "Metal Shop")

SAMPLE_EVENTS = [
    (JSON_EVENT_WITH_VENUE, EVENT_WITH_VENUE),
    (JSON_EVENT_WITH_UNKNOWN_VENUE, EVENT_WITH_UNKNOWN_VENUE),
    (JSON_EVENT_WITHOUT_VENUE, EVENT_WITHOUt_VENUE),
    (COMPLETE_JSON_EVENT, COMPLETE_EVENT),
]

LOCATION_PHRASES = [
    ("Classroom A and B", "Classroom A/B"),
    ("Conference Rm 2", "Conference Room 2"),
    ("Metal shop", "Metal Shop"),
    ("Out Back", "Blacksmithing Alley"),
]

@given(sec_since_epoch = integers(0, END_OF_EPOCH_SEC))
def test_iso_time_converts_back(sec_since_epoch):
    """Test that the ISO time for some seconds since the Unix
    epoch converts as expected."""
    expected_iso_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec_since_epoch))
    converter = EventConverter(None)
    msec_since_epoch = sec_since_epoch * 1000
    iso_time = converter.iso_time(msec_since_epoch)
    assert expected_iso_time == iso_time


@given(event_name = text())
@example(event_name = "AAA: Advanced Anxiety Association")
def test_edit_name_without_prefix(event_name):
    """Test that an unprefixed name edits to the event name."""
    trimmed_event_name = event_name.strip()
    assume(trimmed_event_name)
    converter = EventConverter(None)
    edited_name = converter.edit_name(event_name)
    assert edited_name == trimmed_event_name

@given(prefix = event_prefixes, event_name = event_names)
def test_edit_name_with_prefix(prefix, event_name):
    """Test that a prefixed name edits to the event name."""
    trimmed_event_name = event_name.strip()
    assume(trimmed_event_name)
    converter = EventConverter(None)
    raw_name = "{}: {}".format(prefix, event_name)
    edited_name = converter.edit_name(raw_name)
    assert edited_name == trimmed_event_name

@pytest.mark.parametrize("json_event,expected_event", SAMPLE_EVENTS)
def test_convert(json_event, expected_event):
    """Test converting an event from Meetup JSON into an event tuple."""
    extractor = LocationExtractor.from_location_phrases(LOCATION_PHRASES, "Nova Labs")
    converter = EventConverter(extractor)
    event = converter.convert(json_event)
    assert expected_event == event

def test_timezone():
    """Test that the timezone is set to an expected value."""
    local_time = time.localtime()
    assert local_time.tm_zone in EXPECTED_TIMEZONES

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

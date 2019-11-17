"""Converts Meetup events from JSON dictionaries into event objects."""

from .event_location import EventLocation
import re
import logging
from collections import namedtuple


THREE_HOURS_MSEC = 3 * 60 * 60 * 1000
DEFAULT_DURATION = THREE_HOURS_MSEC
CANCELLED_LOCATION = EventLocation("Cancelled", [])

# Meetup event JSON field names
DURATION_KEY ="duration"
FIND_US_KEY ="how_to_find_us"
MEETUP_ID_KEY ="id"
NAME_KEY ="name"
START_TIME_KEY ="time"
VENUE_KEY ="venue"
VENUE_NAME_KEY ="name"

Event = namedtuple(
        "Event",
        "meetup_id name location start_time end_time places")

PartialEvent = namedtuple(
        "PartialEvent",
        "meetup_id name start_time end_time venue_name find_us")


class EventConverter:

    logger = logging.getLogger("EventConverter")

    def __init__(self, location_chooser, date_time_creator):
        """Initialize with a location chooser, and a date/time creator."""
        self.location_chooser = location_chooser
        self.date_time_creator = date_time_creator

    def convert(self, event_json):
        """Convert Meetup event JSON to an event tuple."""
        partial_event = self.partial_event(event_json)
        event_location = self.location_chooser.choose_location(partial_event)
        self.logger.debug(
                "Location='%s' MeetupEvent=%s", event_location, partial_event)
        return self.event(partial_event, event_location)

    def convert_cancelled(self, event_json):
        """Convert Meetup cancelled event JSON to an event tuple."""
        partial_event = self.partial_event(event_json)
        return self.event(partial_event, CANCELLED_LOCATION)

    def partial_event(self, event_json):
        """Convert Meetup event JSON to a partial event tuple."""
        meetup_id = event_json[MEETUP_ID_KEY]
        name = self.edit_name(event_json[NAME_KEY])
        start_time_epoch_ms = event_json[START_TIME_KEY]
        start_time = self.date_time_creator.xibo_time(start_time_epoch_ms)
        duration = event_json.get(DURATION_KEY, DEFAULT_DURATION)
        end_time = self.date_time_creator.xibo_time(
                start_time_epoch_ms + duration)
        venue = event_json.get(VENUE_KEY, {VENUE_NAME_KEY: ""})
        venue_name = venue[VENUE_NAME_KEY]
        find_us = event_json.get(FIND_US_KEY, "")
        return PartialEvent(
                meetup_id, name, start_time, end_time, venue_name, find_us)

    @staticmethod
    def event(partial_event, location):
        """Return an event combining a partial event and a location."""
        return Event(
            partial_event.meetup_id,
            partial_event.name,
            location.description,
            partial_event.start_time,
            partial_event.end_time,
            location.places)

    @staticmethod
    def edit_name(raw_name):
        """Extract a condensed name, omitting the accounting code."""
        match = re.search(r'^\s*[A-Z3][A-Z]:\s*(\S.*)$', raw_name, re.DOTALL)
        if match:
            name = match.group(1)
        else:
            name = raw_name
        return name.strip()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

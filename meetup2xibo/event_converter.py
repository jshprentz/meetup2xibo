"""Converts Meetup events from JSON dictionaries into event objects."""

import re
from collections import namedtuple
from datetime import datetime


THREE_HOURS_MSEC = 3 * 60 * 60 * 1000

Event = namedtuple("Event", "meetup_id name location start_time end_time")
PartialEvent = namedtuple("PartialEvent", "meetup_id name start_time end_time venue_name find_us")


class EventConverter:

    def __init__(self, location_builder):
        """Initialize with a location builder."""
        self.location_builder = location_builder

    def convert(self, event_json):
        """Convert Meetup event JSON to an event tuple."""
        partial_event = self.partial_event(event_json)
        location = self.location_builder.build_location(partial_event)
        return self.event(partial_event, location)

    def partial_event(self, event_json):
        """Convert Meetup event JSON to a partial event tuple."""
        meetup_id = event_json["id"]
        name = self.edit_name(event_json["name"])
        start_time = self.iso_time(event_json["time"])
        duration = event_json.get("duration", THREE_HOURS_MSEC)
        end_time = self.iso_time(event_json["time"] + duration)
        venue = event_json.get("venue", {"name": ""})
        venue_name = venue["name"]
        find_us = event_json.get("how_to_find_us", "")
        return PartialEvent(meetup_id, name, start_time, end_time, venue_name, find_us)

    @staticmethod
    def event(partial_event, location):
        """Return an event combining a partial event and a location."""
        return Event(
            partial_event.meetup_id,
            partial_event.name,
            location,
            partial_event.start_time,
            partial_event.end_time)
                        

    @staticmethod
    def iso_time(epoch_ms):
        """Format a time represented as milliseconds since the Unix epoch
        in ISO YYYY-MM-DD hh:mm:ss format."""
        return datetime.fromtimestamp(epoch_ms/1000).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def edit_name(raw_name):
        """Extract a condensed name, omitting the accounting code."""
        match = re.search(r'^\s*[A-Z][A-Z]:\s*(\S.*)$', raw_name, re.DOTALL)
        if match:
            name = match.group(1)
        else:
            name = raw_name
        return name.strip()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

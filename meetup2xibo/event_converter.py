"""Converts Meetup events from JSON dictionaries into event objects."""

import re
from collections import namedtuple
from datetime import datetime


THREE_HOURS_MSEC = 3 * 60 * 60 * 1000

Event = namedtuple("Event", "meetup_id name location start_time end_time")


class EventConverter:

    def __init__(self, location_extractor):
        """Initialize with a location extractor."""
        self.location_extractor = location_extractor

    def convert(self, event_json):
        """Convert Meetup event JSON to an event tuple."""
        meetup_id = event_json["id"]
        name = self.edit_name(event_json["name"])
        start_time = self.iso_time(event_json["time"])
        duration = event_json.get("duration", THREE_HOURS_MSEC)
        end_time = self.iso_time(event_json["time"] + duration)
        location = self.extract_location(event_json)
        return Event(meetup_id, name, location, start_time, end_time)

    def extract_location(self, event_json):
        """Extract the location(s) from the Meetup event JSON."""
        venue = event_json.get("venue", {"name": ""})
        venue_name = venue["name"]
        find_us = event_json.get("how_to_find_us", "")
        return self.location_extractor.extract(venue_name, find_us)

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

"""Converts Meetup events from JSON dictionaries into event objects."""

import re
import time
from collections import namedtuple

THREE_HOURS_MSEC = 3 * 60 * 60 * 1000

Event = namedtuple("Event", "meetup_id name start_time end_time location")


class EventConverter:

    def convert(self, event_json):
        """Convert Meetup event JSON to an event tuple."""
        meetup_id = event_json["id"]
        name = self.edit_name(event_json["name"])
        start_time = self.iso_time(event_json["time"])
        duration = event_json.get("duration", THREE_HOURS_MSEC)
        end_time = self.iso_time(event_json["time"] + duration)
        location = "TODO"
        return Event(meetup_id, name, start_time, end_time, location)

    @staticmethod
    def iso_time(epoch_ms):
        """Format a time represented as milliseconds since the Unix epoch
        in ISO YYYY-MM-DD hh:mm:ss format."""
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_ms/1000))

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

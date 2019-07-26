"""Alternate location details for Meetup events with missing, incorrect, or
unknown locations."""

from .event_location import EventLocation
from collections import namedtuple


class SpecialLocation(namedtuple(
        "SpecialLocation",
        "meetup_id location override comment places")):

    """Alternate location details for Meetup events with missing, incorrect, or
    unknown locations."""

    __slots__ = ()

    @property
    def event_location(self):
        """Return an event location."""
        return EventLocation(self.location, self.places)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

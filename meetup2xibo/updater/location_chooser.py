"""Chooses locations for partial events."""

from .event_location import EventLocation
import logging


class LocationChooser:

    """Chooses locations for partial events.

    For events with no special location, prefer any computed location over the
    default.

    For events with a special location and no computed location, prefer any
    special location over the default.

    For events with both an special location and a computed location, if the
    override flag is set, prefer any special location over any computed
    location over the default; otherwise prefer the computed location over the
    special location over the default."""

    logger = logging.getLogger("LocationChooser")

    def __init__(
            self, place_finder, special_locations, default_event_location):
        """Initialize with a place finder, a dictionary of special locations
        (indexed by Meetup ID), and a default event location."""
        self.place_finder = place_finder
        self.special_locations = special_locations
        self.default_event_location = default_event_location

    def choose_location(self, partial_event):
        """Choose a location from a partial Meetup event."""
        computed_event_location = self.find_event_location(partial_event)
        special_location = self.special_locations.get(partial_event.meetup_id)
        return self.resolve_locations(
                partial_event, computed_event_location, special_location)

    def find_event_location(self, partial_event):
        """Find an event location from a partial Meetup event."""
        found_places = self.place_finder.find_places(partial_event)
        return EventLocation.from_places(found_places)

    def resolve_locations(
                self, partial_event, computed_event_location,
                special_location):
        """Choose an appropriate event location based on the availability of a
        special location."""
        if special_location:
            return self.resolve_with_special(
                    computed_event_location, special_location)
        else:
            return self.resolve_without_special(
                    partial_event, computed_event_location)

    def resolve_with_special(self, computed_event_location, special_location):
        """Consider the computed event location and the special location (both
        for a partial event) and the default event location. Return the most
        appropriate event location."""
        if special_location.override:
            best_event_location = special_location.event_location \
                    or computed_event_location \
                    or self.default_event_location
        else:
            best_event_location = computed_event_location \
                    or special_location.event_location \
                    or self.default_event_location
        return best_event_location

    def resolve_without_special(self, partial_event, computed_event_location):
        """Consider computed and the default event locations. Return the most
        appropriate location."""
        if computed_event_location:
            return computed_event_location
        else:
            self.logger.info('Unknown location for %s', partial_event)
            return self.default_event_location

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

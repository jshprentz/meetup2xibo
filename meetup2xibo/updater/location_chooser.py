"""Chooses locations for partial events."""

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

    def __init__(self, location_builder, special_locations, default_location):
        """Initialize with a location builder, a dictionary of special
        locations (indexed by Meetup ID), and a default location."""
        self.location_builder = location_builder
        self.special_locations = special_locations
        self.default_location = default_location

    def choose_location(self, partial_event):
        """Choose a location from a partial Meetup event."""
        computed_location = self.location_builder.build_location(partial_event)
        special_location = self.special_locations.get(partial_event.meetup_id)
        return self.resolve_locations(
                partial_event, computed_location, special_location)

    def resolve_locations(
                self, partial_event, computed_location, special_location):
        """Consider computed and special locations for a partial event and the
        default location. Return the most appropriate location."""
        if special_location:
            return self.resolve_with_special(
                    computed_location, special_location)
        else:
            return self.resolve_without_special(
                    partial_event, computed_location)

    def resolve_with_special(self, computed_location, special_location):
        """Consider computed and the default location. Return the most
        appropriate location."""
        if special_location.override:
            best_location = special_location.location \
                    or computed_location \
                    or self.default_location
        else:
            best_location = computed_location \
                    or special_location.location \
                    or self.default_location
        return best_location

    def resolve_without_special(self, partial_event, computed_location):
        """Consider computed and the default location. Return the most
        appropriate location."""
        if computed_location:
            return computed_location
        else:
            self.logger.info('Unknown location for %s', partial_event)
            return self.default_location


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

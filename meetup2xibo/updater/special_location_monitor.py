"""Monitors special locations and reports when they are not needed."""

import logging


class SpecialLocationMonitor:

    """Monitors special locations and reports when they are not needed."""

    logger = logging.getLogger("SpecialEventsMonitor")

    def __init__(self, special_locations):
        """Initialize with a dictionary of special locations (indexed
        by Meetup ID)."""
        self.special_locations = special_locations

    def deleted_event(self, xibo_event):
        """Log a warning when a deleted Xibo event has a corresponding special
        location."""
        special_location = self.special_locations.get(xibo_event.meetup_id)
        if special_location:
            self.logger.info("No longer needed %s", special_location)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

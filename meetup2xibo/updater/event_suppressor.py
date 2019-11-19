"""Tracks which events should be suppressed and which have been surpressed."""

import logging


class EventSuppressor:

    """Tracks which events should be suppressed and which have been
    surpressed."""

    logger = logging.getLogger("EventSuppressor")

    def __init__(self, meetup_ids_to_suppress):
        """Initialize with a list of Meetup IDs to suppress."""
        self.meetup_ids_to_suppress = frozenset(meetup_ids_to_suppress)
        self.suppressed_meetup_ids = set()

    def should_suppress(self, meetup_id):
        """Given an event's Meetup ID, return true if the event should be
        suppressed; false otherwise."""
        suppress = meetup_id in self.meetup_ids_to_suppress
        if suppress:
            self.suppressed_meetup_ids.add(meetup_id)
        return suppress

    def log_all_ids(self):
        """Log suppressed and unchecked IDs for later reporting."""
        self.log_suppressed_ids()
        self.log_unchecked_ids()

    def log_suppressed_ids(self):
        """Log suppressed Meetup IDs."""
        for meetup_id in self.suppressed_meetup_ids:
            self.log_suppressed_id(meetup_id)

    def log_suppressed_id(self, meetup_id):
        """Log a suppressed Meetup ID."""
        self.logger.info("Suppressed meetup_id=%r", meetup_id)

    def log_unchecked_ids(self):
        """Log Meetup IDs to suppress that never were checked."""
        for meetup_id in self.unchecked_meetup_ids():
            self.log_unchecked_id(meetup_id)

    def unchecked_meetup_ids(self):
        """Return a set of Meetup IDs that should be suppressed, but never were
        checked."""
        return self.meetup_ids_to_suppress - self.suppressed_meetup_ids

    def log_unchecked_id(self, meetup_id):
        """Log an unchecked Meetup ID."""
        self.logger.info(
                "Suppressed Meetup ID was not checked. meetup_id=%r",
                meetup_id)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

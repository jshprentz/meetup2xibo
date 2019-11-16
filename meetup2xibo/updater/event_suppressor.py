"""Tracks which events should be suppressed and which have been surpressed."""

class EventSuppressor:

    """Tracks which events should be suppressed and which have been
    surpressed."""

    def __init__(self, meetup_ids_to_suppress):
        """Initialize with a list of Meetup IDs to suppress."""
        self.meetup_ids_to_suppress = frozenset(meetup_ids_to_suppress)

    def should_suppress(self, meetup_id):
        """Given an event's Meetup ID, return true if the event should be
        suppressed; false otherwise."""
        return meetup_id in self.meetup_ids_to_suppress

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

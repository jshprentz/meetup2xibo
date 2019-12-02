"""Tracks suppressed events, event IDs, and unchecked event IDs."""


class SuppressedEventTracker:

    def __init__(self):
        """Initialize with empty sets of suppressed and unchecked Meetup
        IDs."""
        self._suppressed_ids = set()
        self._unchecked_ids = set()

    def suppressed_id(self, meetup_id):
        """Track the suppression of a Meetup ID."""
        self._suppressed_ids.add(meetup_id)

    def suppressed_event(self, event):
        """Track the suppression of an event. Return the event."""
        self.suppressed_id(event.meetup_id)
        return event

    def unchecked_id(self, meetup_id):
        """Track an unchecked Meetup ID that should be suppressed."""
        self._unchecked_ids.add(meetup_id)

    def unneeded_ids(self):
        """Return a list of suppressed Meetup IDs no longer needed."""
        unneeded_ids = self._unchecked_ids - self._suppressed_ids
        return list(unneeded_ids)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

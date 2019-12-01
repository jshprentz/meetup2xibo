"""Tracks suppressed events, event IDs, and missing event IDs."""


class SuppressedEventTracker:

    def __init__(self):
        """Initialize with empty sets of suppressed and missing Meetup IDs."""
        self._suppressed_ids = set()
        self._missing_ids = set()

    def suppressed_id(self, meetup_id):
        """Track the suppression of a Meetup ID."""
        self._suppressed_ids.add(meetup_id)

    def missing_id(self, meetup_id):
        """Track a missing Meetup ID that should be suppressed."""
        self._missing_ids.add(meetup_id)

    def unneeded_ids(self):
        """Return a list of suppressed Meetup IDs no longer needed."""
        unneeded_ids = self._missing_ids - self._suppressed_ids
        return list(unneeded_ids)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

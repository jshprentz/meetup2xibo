"""An event wrapper that compares events solely by their Meetup ID."""


class MeetupIdComparable:

    """Makes events comparable solely by their Meetup ID."""

    def __init__(self, event):
        """Initialize with an event."""
        self._event = event

    def __eq__(self, other):
        """Test whether Meetup IDs match."""
        return isinstance(other, self.__class__) \
            and self.meetup_id == other.meetup_id

    def __hash__(self):
        """Hash the Meetup ID."""
        return self.meetup_id.__hash__()

    @property
    def event(self):
        """Return the event."""
        return self._event

    @property
    def meetup_id(self):
        """Return the event's Meetup ID."""
        return self._event.meetup_id

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

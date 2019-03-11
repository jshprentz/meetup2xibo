"""Various type of log lines."""


class EventLogLine:

    """A log line reporting an event activity."""

    def __init__(self, timestamp, event):
        """Initialize with a timestamp and an event."""
        self._timestamp = timestamp
        self._event = event

    @property
    def timestamp(self):
        """Return the log line's timestamp."""
        return self._timestamp

    @property
    def event(self):
        """Return the log line's event."""
        return self._event

    @property
    def meetup_id(self):
        """Return the Meetup ID of this log line's event."""
        return self._event.meetup_id

    @property
    def final_event(self):
        """Return the final event from the log line."""
        return self.event


class InsertEventLogLine(EventLogLine):

    """A log line reporting an inserted event."""


class UpdateEventLogLine(EventLogLine):

    """A log line reporting an updated event."""

    def __init__(self, timestamp, before_event, after_event):
        """Initialize with a timestamp and events before and after the
        update. The Meetup ID for both events should be the same."""
        assert before_event.meetup_id == after_event.meetup_id
        super().__init__(timestamp, before_event)
        self._after_event = after_event

    @property
    def before_event(self):
        """Return the log line's before event."""
        return self._event

    @property
    def after_event(self):
        """Return the log line's event."""
        return self._after_event

    @property
    def final_event(self):
        """Return the final event from the log line."""
        return self.after_event


class DeleteEventLogLine(EventLogLine):

    """A log line reporting a deleted event."""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

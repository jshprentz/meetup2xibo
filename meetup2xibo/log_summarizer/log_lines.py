"""Various type of log lines."""


class EventLogLine:

    """A log line reporting an event activity."""

    def __init__(self, timestamp, event, action):
        """Initialize with a timestamp, an event, and an action."""
        self._timestamp = timestamp
        self._event = event
        self._action = action

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

    @property
    def action(self):
        """Return the action description, such as "Inserted"."""
        return self._action

    def add_to_event_crud(self, event_crud):
        """Add this log line to an event CRUD tracker."""
        event_crud.add_log_line(self)


class InsertEventLogLine(EventLogLine):

    """A log line reporting an inserted event."""

    def __init__(self, timestamp, event):
        """Initialize with a timestamp and an event."""
        super().__init__(timestamp, event, "Inserted")


class UpdateEventLogLine(EventLogLine):

    """A log line reporting an updated event."""

    def __init__(self, timestamp, before_event, after_event):
        """Initialize with a timestamp and events before and after the
        update. The Meetup ID for both events should be the same."""
        assert before_event.meetup_id == after_event.meetup_id
        super().__init__(timestamp, before_event, "Updated")
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

    def updates(self):
        """Return a list of updates in (field, before, after) tuple format."""
        return self.before_event.differences(self.after_event)


class DeleteEventLogLine(EventLogLine):

    """A log line reporting a deleted event."""

    def __init__(self, timestamp, event):
        """Initialize with a timestamp and an event."""
        super().__init__(timestamp, event, "Deleted")


class UnknownLocationLogLine(EventLogLine):

    """A log line reporting an unknown locaation."""

    def __init__(self, timestamp, event):
        """Initialize with a timestamp and an event."""
        super().__init__(timestamp, event, "Unknown Location")

    def add_to_event_crud(self, event_crud):
        """Add this log line to an event CRUD tracker."""
        event_crud.add_unknown_location_log_line(self)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Various type of log lines."""


class LogLine:

    """A log line reporting an activity."""

    def __init__(self, timestamp, action):
        """Initialize with a timestamp and an action."""
        self._timestamp = timestamp
        self._action = action

    @property
    def timestamp(self):
        """Return the log line's timestamp."""
        return self._timestamp

    @property
    def action(self):
        """Return the action description, such as "Inserted"."""
        return self._action

    def add_to_event_log(self, event_log):
        """Add this log line to an event log tracker."""
        event_log.add_log_line(self)


class EventLogLine(LogLine):

    """A log line reporting an event activity."""

    def __init__(self, timestamp, event, action):
        """Initialize with a timestamp, an event, and an action."""
        super().__init__(timestamp, action)
        self._event = event

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

    def add_to_event_log(self, event_log):
        """Add this log line to an event log tracker."""
        event_log.add_event_log_line(self)


class CurrentEventLogLine(EventLogLine):

    """A log line reporting an event activity."""

    def add_to_event_log(self, event_log):
        """Add this log line to an event log tracker."""
        super().add_to_event_log(event_log)
        event_log.note_current_event()


class InsertEventLogLine(CurrentEventLogLine):

    """A log line reporting an inserted event."""

    def __init__(self, timestamp, event):
        """Initialize with a timestamp and an event."""
        super().__init__(timestamp, event, "Inserted")


class UpdateEventLogLine(CurrentEventLogLine):

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


class DeleteEventLogLine(CurrentEventLogLine):

    """A log line reporting a deleted event."""

    def __init__(self, timestamp, event):
        """Initialize with a timestamp and an event."""
        super().__init__(timestamp, event, "Deleted")


class RetireEventLogLine(EventLogLine):

    """A log line reporting a retired event."""

    def __init__(self, timestamp, event):
        """Initialize with a timestamp and an event."""
        super().__init__(timestamp, event, "Retired")


class UnknownLocationLogLine(EventLogLine):

    """A log line reporting an unknown locaation."""

    def __init__(self, timestamp, event):
        """Initialize with a timestamp and an event."""
        super().__init__(timestamp, event, "Unknown Location")

    def add_to_event_log(self, event_log):
        """Add this log line to an event log tracker."""
        event_log.add_unknown_location_log_line(self)
        event_log.note_current_event()


class SpecialLocationLogLine(LogLine):

    """A log line reporting an special locaation."""

    def __init__(self, timestamp, special_location):
        """Initialize with a timestamp and an event."""
        super().__init__(timestamp, "Special Location Concluded")
        self._special_location = special_location

    @property
    def special_location(self):
        """Return the log line's special location."""
        return self._special_location

    @property
    def meetup_id(self):
        """Return the Meetup ID of this log line's speical location."""
        return self.special_location.meetup_id


class EventLocationLogLine(EventLogLine):

    """A log line reporting an event location mapping."""

    def __init__(self, timestamp, location, event):
        """Initialize with a timestamp, a location, and an event."""
        super().__init__(timestamp, event, "Event Location")
        self._location = location

    @property
    def location(self):
        """Return the log line's location."""
        return self._location

    def key_fields(self):
        """Return a tuple of key fields to distinguish location mappings of
        interest."""
        return (self.location, self.event.venue, self.event.find_us)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

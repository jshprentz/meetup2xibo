"""Conflicts when two or more events are scheduled in the same place at the
same time."""

from .event import Event


class Conflict:

    """Conflicts when two or more events are scheduled in the same place at the
    same time."""

    def __init__(self, start_time, end_time, events, **other_fields):
        """Initialize with field values of concern."""
        self._start_time = start_time
        self._end_time = end_time
        self._events = events

    @classmethod
    def from_fields(cls, field_list):
        """Make an event from a list for (name, value) field tuples."""
        field_dict = dict(field_list)
        return cls(**field_dict)

    def __eq__(self, other):
        """Test with this event equals another."""
        if self is other:
            return True
        elif type(self) != type(other):
            return False
        else:
            return self._start_time == other._start_time \
                and self._end_time == other._end_time \
                and self._events == other._events

    def __hash__(self):
        """Hash the contents of this event."""
        return hash((self._start_time, self._end_time, tuple(self._events)))

    def __repr__(self):
        """Return the debugging representation of this event."""
        return "{}(start_time={!r}, end_time={!r}, events={!r})" \
            .format(self.__class__.__name__,
                    self._start_time, self._end_time, self._events)

    def report_sort_key(self):
        """Return a sort key for sorting into reporting order."""
        return (self._start_time, self._end_time)

    def sorted_events(self):
        """Return the list of events sorted for reporting."""
        return sorted(self._events, key=Event.report_sort_key)

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def events(self):
        return self._events

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

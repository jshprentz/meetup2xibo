"""Meetup and Xibo events store, compare, and report fields."""


MEETUP_EVENT_URL_TEMPLATE = "https://www.meetup.com/NOVA-Makers/events/{}/"


class Event:

    """Meetup and Xibo events store, compare, and report fields."""

    def __init__(
            self, name, location, start_time, end_time, meetup_id,
            **other_fields):
        """Initialize with field values of concern."""
        self._name = name
        self._location = location
        self._start_time = start_time
        self._end_time = end_time
        self._meetup_id = meetup_id

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
            return self._name == other._name \
                and self._location == other._location \
                and self._start_time == other._start_time \
                and self._end_time == other._end_time \
                and self._meetup_id == other._meetup_id

    def __hash__(self):
        """Hash the contents of this event."""
        return hash((
                self._name, self._location, self._start_time, self._end_time,
                self._meetup_id))

    def report_sort_key(self):
        """Return a sort key for sorting into reporting order."""
        return (
            self._name.lower(),
            self._location.lower(),
            self._start_time,
            self._end_time)

    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def meetup_id(self):
        return self._meetup_id

    @property
    def url(self):
        """Return the Meetup URL for this event."""
        return MEETUP_EVENT_URL_TEMPLATE.format(self._meetup_id)

    def differences(self, other):
        """Return a list of differences between this and another later event in
        (field, before, after) tuple format."""
        differences = []
        if self._name != other._name:
            differences.append((
                    "name", self._name, other._name))
        if self._location != other._location:
            differences.append((
                    "location", self._location, other._location))
        if self._start_time != other._start_time:
            differences.append((
                    "start_time", self._start_time, other._start_time))
        if self._end_time != other._end_time:
            differences.append((
                    "end_time", self._end_time, other._end_time))
        if self._meetup_id != other._meetup_id:
            differences.append((
                    "meetup_id", self._meetup_id, other._meetup_id))
        return differences

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

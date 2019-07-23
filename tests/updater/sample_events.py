"""Provides sample events for testing."""

from meetup2xibo.updater.event_converter import Event

# Sample dates and times

D1T1 = "2019-07-01 11:00:00"
D1T2 = "2019-07-01 12:00:00"
D1T3 = "2019-07-01 13:00:00"
D1T4 = "2019-07-01 14:00:00"
D1T5 = "2019-07-01 15:00:00"

D2T1 = "2019-07-02 11:00:00"
D2T2 = "2019-07-02 12:00:00"
D2T3 = "2019-07-02 13:00:00"
D2T4 = "2019-07-02 14:00:00"
D2T5 = "2019-07-02 15:00:00"

D3T1 = "2019-07-03 11:00:00"
D3T2 = "2019-07-03 12:00:00"
D3T3 = "2019-07-03 13:00:00"
D3T4 = "2019-07-03 14:00:00"
D3T5 = "2019-07-03 15:00:00"


class SampleEvents:

    """Makes sample events and event lists."""

    def __init__(self):
        """Initialize with zero events."""
        self.event_count = 0

    def make_event(self, start_time, end_time, places=[]):
        """Make an event starting and ending at the given date/time strings and
        optionally scheduled at a list of place names."""
        self.event_count += 1
        return Event(
            meetup_id = "m{:06d}".format(self.event_count),
            name = "Event {}".format(self.event_count),
            start_time = start_time,
            end_time = end_time,
            places = places,
            location = "Location {}".format(self.event_count))

    def make_sample_sortable_events(self):
        """Make a list of events to test sorting by time and Meetup ID."""
        event1 = self.make_event(D1T1, D1T2)
        event2 = self.make_event(D1T3, D1T4)
        event3 = self.make_event(D1T3, D1T4)
        event4 = self.make_event(D1T3, D1T4)
        event5 = self.make_event(D2T1, D2T2)
        return [event3, event5, event1, event2, event4]

    def make_events(self, n, start_time, end_time, places=[]):
        """Return a list of n events with the same start and end times and
        places."""
        return [self.make_event(start_time, end_time, places=[]) for i in range(n)]

    def make_early_events(self, n):
        """Return a list of n events with identical early start and end
        times."""
        return self.make_events(n, D1T1, D1T2)

    def make_late_events(self, n):
        """Return a list of n events with identical early start and end
        times."""
        return self.make_events(n, D1T3, D1T4)

    def make_non_overlapping_events(self, places=[]):
        """Return two non overlapping events."""
        return (self.make_event(D1T1, D1T2, places),
                self.make_event(D1T3, D1T4, places))

    def make_overlapping_events(self, places=[]):
        """Return two overlapping events."""
        return (self.make_event(D1T1, D1T3, places),
                self.make_event(D1T2, D1T4, places))

    def make_consecutive_events(self, places=[]):
        """Return two events with the first event ending when the second
        starts."""
        return (self.make_event(D2T1, D2T2, places),
                self.make_event(D2T2, D2T3, places))

    def make_straddling_events(self, places=[]):
        """Return two events with the first event starting before and ending
        after the other."""
        return (self.make_event(D2T1, D2T4, places),
                self.make_event(D2T2, D2T3, places))

    def make_same_start_events(self, places=[]):
        """Return two events with the same start time."""
        return (self.make_event(D3T1, D3T2, places),
                self.make_event(D3T1, D3T4, places))

    def make_same_end_events(self, places=[]):
        """Return two events with the same end time."""
        return (self.make_event(D3T3, D3T5, places),
                self.make_event(D3T4, D3T5, places))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

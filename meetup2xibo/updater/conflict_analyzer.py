"""Analyzes events scheduled at places, checking for conflicts."""

from .places import CheckedPlace
from operator import attrgetter
import logging


class ConflictAnalyzer:

    """Analyzes events scheduled at places, checking for conflicts."""

    logger = logging.getLogger("ConflictAnalyzer")

    def __init__(self, conflict_places):
        """Initialize with conflict places."""
        self.conflict_places = conflict_places

    def analyze_conflicts(self, events):
        """Analyze place scheduling conflicts among a list of events."""
        start_events = self.events_by_start_time(events)
        end_events = self.events_by_end_time(events)
        self.analyze_events(start_events, end_events)

    def analyze_events(self, start_events, end_events):
        """Analyze the events listed by start and end times."""

    def analyze_events_at_start_time(self, start_events, start_time):
        """Remove and analyze events scheduled at a start time."""
        while start_events and start_events[-1].start_time == start_time:
            self.conflict_places.start_event(start_events.pop())

    def analyze_events_at_end_time(self, end_events, end_time):
        """Remove and analyze events scheduled at a end time."""
        while end_events and end_events[-1].end_time == end_time:
            self.conflict_places.end_event(end_events.pop())


    @staticmethod
    def events_by_start_time(events):
        """Return the list of events sorted by start time (and Meetup ID for
        consistent disambiguation)."""
        return sorted(
                events,
                key=attrgetter('start_time', 'meetup_id'),
                reverse=True)

    @staticmethod
    def events_by_end_time(events):
        """Return the list of events sorted by end time (and Meetup ID for
        consistent disambiguation)."""
        return sorted(
                events,
                key=attrgetter('end_time', 'meetup_id'),
                reverse=True)

class NullConflictAnalyzer:

    """Skips time consuming analysis."""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

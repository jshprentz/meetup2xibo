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

    @staticmethod
    def events_by_start_time(events):
        """Return the list of events sorted by start time (and Meetup ID for
        consistent disambiguation)."""
        return sorted(events, key=attrgetter('start_time', 'meetup_id'))

    @staticmethod
    def events_by_end_time(events):
        """Return the list of events sorted by end time (and Meetup ID for
        consistent disambiguation)."""
        return sorted(events, key=attrgetter('end_time', 'meetup_id'))

class NullConflictAnalyzer:

    """Skips time consuming analysis."""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

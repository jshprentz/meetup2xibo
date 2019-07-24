"""Analyzes events scheduled at places, checking for conflicts."""

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
        self.logger.info("Start conflict analysis")
        self.log_place_names()
        self.sort_and_analyze_events(events)

    def sort_and_analyze_events(self, events):
        """Sort events by start and end times before analyzing them."""
        start_events = self.events_by_start_time(events)
        end_events = self.events_by_end_time(events)
        self.analyze_events(start_events, end_events)

    def analyze_events(self, start_events, end_events):
        """Analyze the events listed by start and end times."""
        self.analyze_start_and_end_events(start_events, end_events)
        self.analyze_start_events(start_events)
        self.analyze_end_events(end_events)

    def analyze_start_and_end_events(self, start_events, end_events):
        """Analyze events while both start and end events remain."""
        while start_events and end_events:
            clock = self.earliest_time(start_events, end_events)
            self.analyze_events_at_start_time(start_events, clock)
            self.analyze_events_at_end_time(end_events, clock)
            self.log_conflicts(clock)

    def analyze_start_events(self, start_events):
        """Analyze events while both start events remain."""
        while start_events:
            clock = start_events[-1].start_time
            self.analyze_events_at_start_time(start_events, clock)
            self.log_conflicts(clock)

    def analyze_end_events(self, end_events):
        """Analyze events while both end events remain."""
        while end_events:
            clock = end_events[-1].end_time
            self.analyze_events_at_end_time(end_events, clock)
            self.log_conflicts(clock)

    def analyze_events_at_start_time(self, start_events, start_time):
        """Remove and analyze events scheduled at a start time."""
        while start_events and start_events[-1].start_time == start_time:
            self.conflict_places.start_event(start_events.pop())

    def analyze_events_at_end_time(self, end_events, end_time):
        """Remove and analyze events scheduled at a end time."""
        while end_events and end_events[-1].end_time == end_time:
            self.conflict_places.end_event(end_events.pop())

    def log_conflicts(self, clock):
        """Log accumulated conflicts ending at a clock time."""
        self.conflict_places.log_conflicts(clock)

    def log_place_names(self):
        """Log place names."""
        self.conflict_places.log_place_names()

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

    @staticmethod
    def earliest_time(start_events, end_events):
        """Return the earliest start or end event time from lists ordered in
        reverse by start and end times."""
        return min(start_events[-1].start_time, end_events[-1].end_time)


class NullConflictAnalyzer:

    """Skips time consuming analysis."""

    def analyze_conflicts(self, events):
        """Do not analyze place scheduling conflicts among a list of events."""
        pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

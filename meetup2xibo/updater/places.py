"""Places for schedule conflict checking."""

from .meetup_id_comparable import MeetupIdComparable
from .exceptions import ContainmentLoopError
from collections import namedtuple, Counter
from operator import attrgetter
import logging


Conflict = namedtuple(
        "Conflict",
        "start_time end_time events")


class ContainingPlace:

    """ A place that may contain other places."""

    logger = logging.getLogger("ContainingPlace")

    def __init__(self, name):
        """Initialize with a place name."""
        self.name = name
        self.contained_places = set()
        self.containing_places = set()

    def __repr__(self):
        """Return the debugging representation of a containing place."""
        return '{}({!r})'.format(
                self.__class__.__name__,
                self.name)

    def contain(self, other_place):
        """Contain the other place within this place."""
        self.contained_places.add(other_place)
        other_place.containing_places.add(self)

    def contains(self, other_place):
        """Return true if this place contains the other place; false
        otherwise."""
        return other_place in self.contained_places

    def start_event_carefully(self, event):
        """Start an event at this place, checking for containment loops."""
        try:
            self.start_event(event)
        except RecursionError:
            raise ContainmentLoopError(self.containment_loop_message())

    def start_event_in_contained_places(self, event):
        """Start an event in places contained within this place."""
        for place in self.contained_places:
            place.start_event(event)

    def end_event_carefully(self, event):
        """End an event at this place, checking for containment loops."""
        try:
            self.end_event(event)
        except RecursionError:
            raise ContainmentLoopError(self.containment_loop_message())

    def end_event_in_contained_places(self, event):
        """End an event in places contained within this place."""
        for place in self.contained_places:
            place.end_event(event)

    def container_has_conflict(self, conflict):
        """Return true if any containing place has the same conflict as the
        given conflict."""
        for place in self.containing_places:
            if place.has_conflict(conflict):
                return True
        return False

    def containment_loop_message(self):
        """Return a containment loop error message for this place."""
        return "Loop found among containing places. Check {!r}." \
            .format(self.name)

    def log_place_name(self):
        """Log the name of this place."""
        self.logger.info("Name=%r", self.name)


class CheckedPlace(ContainingPlace):

    """A placed checked for conflicts."""

    logger = logging.getLogger("CheckedPlace")

    def __init__(self, name):
        """Initialize with a place name."""
        super().__init__(name)
        self.clock = ""
        self.events = Counter()
        self.conflict = None

    def start_event(self, event):
        """Start an event at this place."""
        self.advance_clock(event.start_time)
        self.count_event(event, 1)
        self.start_event_in_contained_places(event)

    def end_event(self, event):
        """End an event at this place."""
        self.advance_clock(event.end_time)
        self.count_event(event, -1)
        self.end_event_in_contained_places(event)

    def advance_clock(self, new_time):
        """Advance the clock to the new time. Note conflicts when clock
        changes."""
        if (self.clock == new_time):
            return
        old_time = self.clock
        self.clock = new_time
        self.note_conflicts(old_time, new_time)

    def count_event(self, event, increment):
        """Increment the event's count."""
        comparable_event = MeetupIdComparable(event)
        self.events[comparable_event] += increment

    def note_conflicts(self, start_time, end_time):
        """Note conflicting events scheduled during the interval from the start
        time to the end time."""
        self.events = +self.events
        if len(self.events) > 1:
            self.conflict = self.make_conflict(start_time, end_time)

    def make_conflict(self, start_time, end_time):
        """Make a end conflict tuple from current events and the time
        interval."""
        sorted_events = sorted(list(self.events), key=attrgetter('meetup_id'))
        return Conflict(start_time, end_time, tuple(sorted_events))

    def has_conflict(self, conflict):
        """Return true if this place has the same conflict as the given
        conflict."""
        return conflict == self.conflict

    def log_conflicts(self, end_time):
        """Log conflict found during event analysis if it matches the end
        time."""
        if self.conflict \
                and self.conflict.end_time == end_time \
                and not self.container_has_conflict(self.conflict):
            reportable_conflict = Conflict(
                self.conflict.start_time,
                self.conflict.end_time,
                [comparable.event for comparable in self.conflict.events])
            self.logger.info(
                    "Schedule conflict: place=%r %s",
                    self.name, reportable_conflict)


class UncheckedPlace(ContainingPlace):

    """A placed not checked for conflicts."""

    logger = logging.getLogger("UncheckedPlace")

    def start_event(self, event):
        """Start an event at this place."""
        self.start_event_in_contained_places(event)

    def end_event(self, event):
        """End an event at this place."""
        self.end_event_in_contained_places(event)

    def has_conflict(self, conflict):
        """Return true if any of this place's containers have the same conflict
        as the given conflict."""
        return self.container_has_conflict(conflict)

    def log_conflicts(self, end_time):
        """Log no conflicts from unchecked places."""
        pass


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

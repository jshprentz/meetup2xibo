"""Places for schedule conflict checking."""

import logging

class ContainingPlace:

    """ A place that may contain other places."""

    def __init__(self, name):
        """Initialize with a place name."""
        self._name = name
        self._contained_places = set()

    def __repr__(self):
        """Return the debugging representation of a containing place."""
        return '{}({!r})'.format(
                self.__class__.__name__,
                self._name)

    def contain(self, other_place):
        """Contain the other place within this place."""
        self._contained_places.add(other_place)

    def contains(self, other_place):
        """Return true if this place contains the other place; false
        otherwise."""
        return other_place in self._contained_places

    def start_event(self, event):
        """Analyze the start of an event at this place."""

    def end_event(self, event):
        """Analyze the end of an event at this place."""

    def log_conflicts(self):
        """Log conflicts found during event analysis."""



class CheckedPlace(ContainingPlace):

    """A placed checked for conflicts."""

    logger = logging.getLogger("CheckedPlace")


class UncheckedPlace(ContainingPlace):

    """A placed not checked for conflicts."""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Collect and reports on scheduling conflicts."""

from collections import defaultdict


class ConflictReporter:

    """Collects and reports scheduling conflicts organized by place and
    time."""

    def __init__(self):
        """Initialize with no conflicts or places."""
        self._checked_places = []

    def clear(self):
        """Clear previously collected conflicts and places to start a new
        analysis."""
        self._checked_places.clear()

    def add_checked_place(self, name):
        """Add the named checked place."""
        self._checked_places.append(name)

    def add_conflict(self, conflict):
        """Add the scheduling conflict."""
        pass

    def has_conflicts(self):
        """Return true if there are scheduling conflicts; false otherwise."""
        return False

    def sorted_checked_places(self):
        """Return a sorted list of checked places."""
        return sorted(self._checked_places)

    def sorted_conflict_places(self):
        """Return a sorted list of places with their conflicts."""
        return []


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

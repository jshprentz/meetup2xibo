"""Counts program starts."""


class StartCounter:

    """Counts program starts."""

    def __init__(self):
        """Initialize with no counters."""
        self.counters = {}

    def count(self, name):
        """Count the start of a named program."""
        prev_count = self.counters.get(name, 0)
        self.counters[name] = prev_count + 1

    def counts(self):
        """Return a sorted list of (name, count) tuples."""
        tuples = list(self.counters.items())
        tuples.sort()
        return tuples


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

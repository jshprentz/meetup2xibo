"""Collects mappings of venue/find-us to location in log lines."""


class LocationMapper:

    """Collects mappings of venue/find-us to location in log lines."""

    def __init__(self):
        """Initialize with no mappings."""
        self._mappings = {}

    def add_event_location_log_line(self, log_line):
        """Add the log line's mapping to the list."""
        key_fields = log_line.key_fields()
        self._mappings[key_fields] = log_line

    def has_mappings(self):
        """Return true if there are location mappings; false otherwise."""
        return bool(self._mappings)

    def mapping_list(self):
        """Return a list of log lines showing the mapping from
        venue/find-us to location."""
        sorted_keys = sorted(self._mappings.keys())
        return [self._mappings[key] for key in sorted_keys]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

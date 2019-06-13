"""Collects and reports event log activity."""


class EventLog:

    """Collects and reports event log activity."""

    def __init__(self):
        """Initialize ..."""
        self._log_lines = []
        self._last_unknown_location_event = None
        self._final_event = None
        self._sort_key = None
        self._current_event_flag = False

    @property
    def log_lines(self):
        """Return the list of log lines."""
        return self._log_lines

    @property
    def final_event(self):
        """Return the final event from the log line list."""
        return self._final_event

    def add_log_line(self, log_line):
        """Add a log line to the list."""
        self._log_lines.append(log_line)

    def add_event_log_line(self, log_line):
        """Add a log line to the list."""
        self._final_event = log_line.final_event
        self.add_log_line(log_line)

    def add_unknown_location_log_line(self, log_line):
        """Add an unknown location log line to the list if changed."""
        if log_line.event != self._last_unknown_location_event:
            self._last_unknown_location_event = log_line.event
            self.add_event_log_line(log_line)

    def note_current_event(self):
        """Note that there is a current event in the log."""
        self._current_event_flag = True

    def has_current_event(self):
        """Return true if the log contains a current event."""
        return self._current_event_flag

    def report_sort_key(self):
        """Return a key for sorting into report order."""
        if self._sort_key is None:
            self._sort_key = self.final_event.report_sort_key()
        return self._sort_key


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

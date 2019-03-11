"""Collects and reports event CRUD activity."""

class EventCrud:

    """Collects and reports event CRUD activity."""

    def __init__(self):
        """Initialize ..."""
        self._log_lines = []

    @property
    def log_lines(self):
        """Return the list of log lines."""
        return self._log_lines

    @property
    def final_event(self):
        """Return the final event from the log line list."""
        return self._log_lines[-1].final_event

    def add_log_line(self, log_line):
        """Add a log line to the list."""
        self._log_lines.append(log_line)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

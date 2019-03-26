"""Collects and lists CRUD event log lines."""

from .event_log import EventLog
from collections import defaultdict


class CrudLister:

    """Collects and lists CRUD event log lines organized by Meetup event."""

    def __init__(self):
        """Initialize with no Meetup event CRUDs."""
        self.event_logs = defaultdict(EventLog)

    def add_log_line(self, log_line):
        """Add a log line."""
        event_log = self.event_logs[log_line.meetup_id]
        log_line.add_to_event_log(event_log)

    def sorted_current_event_logs(self):
        """Return a list of current event logs sorted for reporting."""
        event_log_list = [
                event_log for event_log in self.event_logs.values()
                if event_log.has_current_event()]
        event_log_list.sort(key=EventLog.report_sort_key)
        return event_log_list

    def sorted_past_event_logs(self):
        """Return a list of past event logs sorted for reporting."""
        event_log_list = [
                event_log for event_log in self.event_logs.values()
                if not event_log.has_current_event()]
        event_log_list.sort(key=EventLog.report_sort_key)
        return event_log_list


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

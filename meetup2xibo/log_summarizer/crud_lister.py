"""Collects and lists CRUD event log lines."""

from .event import Event
from .event_crud import EventCrud
from .log_lines import InsertEventLogLine, UpdateEventLogLine, DeleteEventLogLine
from collections import defaultdict


class CrudLister:

    """Collects and lists CRUD event log lines organized by Meetup event."""

    def __init__(self):
        """Initialize with no Meetup event CRUDs."""
        self.event_cruds = defaultdict(EventCrud)

    def add_log_line(self, log_line):
        """Add a log line."""
        event_crud = self.event_cruds[log_line.meetup_id]
        event_crud.add_log_line(log_line)

    def sorted_event_cruds(self):
        """Return a list of event cruds sorted for reporting."""
        crud_list = list(self.event_cruds.values())
        crud_list.sort(key=EventCrud.report_sort_key)
        return crud_list


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
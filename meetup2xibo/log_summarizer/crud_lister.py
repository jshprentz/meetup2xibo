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

    def add_log_line(self, meetup_id, log_line):
        """Add a log line for the event identified by a Meetup ID."""
        event_crud = self.event_cruds[meetup_id]
        event_crud.add_log_line(log_line)

    def add_insert_event(self, date_time, fields):
        """Add an insert event log line with a date/time and a list of field
        (name, value) tuples."""
        event = Event.from_fields(fields)
        log_line = InsertEventLogLine(date_time, event)
        self.add_log_line(event.meetup_id, log_line)

    def add_update_event(self, date_time, before_fields, after_fields):
        """Add an update event log line with a date/time and a list of field
        (name, value) tuples."""
        before_event = Event.from_fields(before_fields)
        after_event = Event.from_fields(after_fields)
        log_line = UpdateEventLogLine(date_time, before_event, after_event)
        self.add_log_line(after_event.meetup_id, log_line)

    def add_delete_event(self, date_time, fields):
        """Add a delete event log line with a date/time and a list of field
        (name, value) tuples."""
        event = Event.from_fields(fields)
        log_line = DeleteEventLogLine(date_time, event)
        self.add_log_line(event.meetup_id, log_line)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

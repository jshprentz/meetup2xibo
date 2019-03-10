"""Collects and lists CRUD event log lines."""

class CrudLister:

    """Collects and lists CRUD event log lines."""

    def __init__(self):
        """Initialize ..."""

    def add_insert_event(self, date_time, fields):
        """Add an insert event log line with a date/time and a list of field
        (name, value) tuples."""

    def add_update_event(self, date_time, before_fields, after_fields):
        """Add an update event log line with a date/time and a list of field
        (name, value) tuples."""

    def add_delete_event(self, date_time, fields):
        """Add a delete event log line with a date/time and a list of field
        (name, value) tuples."""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

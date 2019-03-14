"""Event representations in Xibo."""

from collections import namedtuple


XiboEvent = namedtuple(
        "XiboEvent",
        "meetup_id name location start_time end_time xibo_id")


class XiboEventColumnNameManager:

    """Manages event conversion based on column names."""

    def __init__(self, column_names):
        """Initialize with the column names (in a XiboEvent
        tuple) use in Xibo JSON responses."""
        self.column_names = column_names

    def json_to_xibo_event(self, json_event):
        """Convert a JSON event dictionary (or other mapping)
        to a XiboEvent named tuple."""
        return XiboEvent(
            xibo_id=json_event[self.column_names.xibo_id],
            meetup_id=json_event[self.column_names.meetup_id],
            name=json_event[self.column_names.name],
            location=json_event[self.column_names.location],
            start_time=json_event[self.column_names.start_time],
            end_time=json_event[self.column_names.end_time],
        )

    def json_to_column_ids(self, json_columns):
        """Convert JSON metatadata about Xibo dataset columns
        into a XiboEvent loaded with column IDs."""
        heading_to_id_map = {
            column["heading"]:
                "dataSetColumnId_{}".format(column["dataSetColumnId"])
            for column in json_columns
            }
        heading_to_id_map[self.column_names.xibo_id] = None
        return self.json_to_xibo_event(heading_to_id_map)


class XiboEventColumnIdManager:

    """Manages event conversion based on column IDs."""

    def __init__(self, column_ids):
        """Initialize with the column IDs (in a XiboEvent
        tuple) needed for inserting and updating Xibo dataset
        rows."""
        self.column_ids = column_ids

    def event_to_columns(self, event):
        """Convert an event to a dictionary of columns keyed by
        column ID."""
        return {
            self.column_ids.meetup_id: event.meetup_id,
            self.column_ids.name: event.name,
            self.column_ids.location: event.location,
            self.column_ids.start_time: event.start_time,
            self.column_ids.end_time: event.end_time
        }


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

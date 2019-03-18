"""Create, read, update, and delete events in Xibo."""

import logging


class XiboEventCrud:

    """Create, read, update, and delete events in Xibo."""

    logger = logging.getLogger("XiboEventCrud")

    def __init__(
            self, xibo_api, dataset_id, column_name_manager,
            column_id_manager):
        """Initialize with a Xibo API, a dataset ID, and a column name
        manager."""
        self.xibo_api = xibo_api
        self.dataset_id = dataset_id
        self.column_name_manager = column_name_manager
        self.column_id_manager = column_id_manager

    def get_xibo_events(self):
        """Get a list of events from Xibo."""
        xibo_json = self.xibo_api.get_dataset_data_by_id(self.dataset_id)
        return (
            self.column_name_manager.json_to_xibo_event(event_json)
            for event_json in xibo_json
            )

    def delete_xibo_event(self, xibo_event, action="Deleted"):
        """Delete a Xibo event and log the action."""
        self.xibo_api.delete_dataset_data_by_id(
            self.dataset_id, xibo_event.xibo_id)
        self.logger.info("%s %s", action, xibo_event)

    def insert_meetup_event(self, meetup_event):
        """Insert a Meetup event into the database."""
        columns = self.column_id_manager.event_to_columns(meetup_event)
        self.xibo_api.insert_dataset_data(self.dataset_id, columns)
        self.logger.info("Inserted %s", meetup_event)

    def update_xibo_event(self, xibo_event, meetup_event):
        """Update a Xibo event with a Meetup event."""
        row_id = xibo_event.xibo_id
        columns = self.column_id_manager.event_to_columns(meetup_event)
        self.xibo_api.update_dataset_data(self.dataset_id, row_id, columns)
        self.logger.info("Updated from %s", xibo_event)
        self.logger.info("Updated to %s", meetup_event)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

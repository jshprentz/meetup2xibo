"""Updates the events in the Xibo database to conform to events from Meetup.com."""


class EventUpdater:

    """Updates events in a Xibo database by inserting, updating, or deleting 
    events to make the Xibo events conform to Meetup.com events."""

    def __init__(self, meetup_events, xibo_events, db_connection):
        """Initialize with lists (or iterables) of Meetup and Xibo events
        and a Xibo database connection."""
        self.meetup_events = self.event_list_to_dict(meetup_events)
        self.xibo_events = self.event_list_to_dict(xibo_events)
        self.db_connection = db_connection

    def update_xibo(self):
        """Update the Xibo database by inserting, updating, or deleting
        events to make the Xibo events conform to Meetup.com events."""
        ids_from_meetup = set(self.meetup_events.keys())
        ids_from_xibo = set(self.xibo_events.keys())
        self.update_known_events(ids_from_meetup & ids_from_xibo)
        self.insert_new_events(ids_from_meetup - ids_from_xibo)
        self.delete_unknown_events(ids_from_xibo - ids_from_meetup)

    def update_known_events(self, event_ids):
        """Update changed events given a set of event IDs."""
        for event_id in event_ids:
            xibo_event = self.xibo_events[event_id]
            meetup_event = self.meetup_events[event_id]
            self.update_changed_event(xibo_event, meetup_event)

    def update_changed_event(self, xibo_event, meetup_event):
        """Update the Xibo event with data from the Meetup event if they differ."""
        if xibo_event.name == meetup_event.name \
                and xibo_event.location == meetup_event.location \
                and xibo_event.start_time == meetup_event.start_time \
                and xibo_event.end_time == meetup_event.end_time:
            return
        self.db_connection.update_xibo_event(xibo_event, meetup_event)

    def insert_new_events(self, event_ids):
        """Insert new events given a set of event IDs."""
        for event_id in event_ids:
            meetup_event = self.meetup_events[event_id]
            self.db_connection.insert_meetup_event(meetup_event)

    def delete_unknown_events(self, event_ids):
        """Delete unknown (to Meetup) events given a set of event IDs."""
        for event_id in event_ids:
            xibo_event = self.xibo_events[event_id]
            self.db_connection.delete_xibo_event(xibo_event)

    @staticmethod
    def event_list_to_dict(events):
        return {event.meetup_id: event for event in events}


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
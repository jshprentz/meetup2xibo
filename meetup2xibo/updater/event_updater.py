"""Updates the events in the Xibo database to conform to events from
Meetup.com."""

from .anti_flapper import EventFlappingStatus
import logging


class EventUpdater:

    """Updates events in a Xibo dataset by inserting, updating, or deleting
    events to make the Xibo events conform to Meetup.com events."""

    logger = logging.getLogger("EventUpdater")

    def __init__(
                self, meetup_events, cancelled_meetup_events, xibo_events,
                xibo_event_crud, anti_flapper, special_location_monitor):
        """Initialize with lists (or iterables) of Meetup and Xibo events, a
        Xibo event CRUD manager, an anti-flapper, and a special location
        monitor."""
        self.meetup_events = self.event_list_to_dict(meetup_events)
        self.cancelled_meetup_events = self.event_list_to_dict(
                cancelled_meetup_events)
        self.xibo_events = self.event_list_to_dict(xibo_events)
        self.xibo_event_crud = xibo_event_crud
        self.anti_flapper = anti_flapper
        self.special_location_monitor = special_location_monitor

    def update_xibo(self):
        """Update the Xibo database by inserting, updating, or deleting
        events to make the Xibo events conform to Meetup.com events."""
        ids_from_meetup = set(self.meetup_events.keys())
        ids_cancelled_from_meetup = set(self.cancelled_meetup_events.keys())
        ids_from_xibo = set(self.xibo_events.keys())
        self.update_known_events(ids_from_meetup & ids_from_xibo)
        self.update_cancelled_events(ids_cancelled_from_meetup & ids_from_xibo)
        self.insert_new_events(ids_from_meetup - ids_from_xibo)
        self.delete_unknown_events(
                ids_from_xibo - ids_from_meetup - ids_cancelled_from_meetup)

    def update_known_events(self, event_ids):
        """Update changed events given a set of event IDs."""
        for event_id in event_ids:
            xibo_event = self.xibo_events[event_id]
            meetup_event = self.meetup_events[event_id]
            self.update_changed_event(xibo_event, meetup_event)

    def update_cancelled_events(self, event_ids):
        """Update changed events given a set of cancelled event IDs."""
        for event_id in event_ids:
            xibo_event = self.xibo_events[event_id]
            meetup_event = self.cancelled_meetup_events[event_id]
            self.update_changed_event(xibo_event, meetup_event)

    def update_changed_event(self, xibo_event, meetup_event):
        """Update the Xibo event with data from the Meetup event if they
        differ."""
        if xibo_event.name == meetup_event.name \
                and xibo_event.location == meetup_event.location \
                and xibo_event.start_time == meetup_event.start_time \
                and xibo_event.end_time == meetup_event.end_time:
            self.logger.debug("Unchanged %s", xibo_event)
            return
        self.xibo_event_crud.update_xibo_event(xibo_event, meetup_event)

    def insert_new_events(self, event_ids):
        """Insert new events given a set of event IDs."""
        for event_id in event_ids:
            meetup_event = self.meetup_events[event_id]
            self.xibo_event_crud.insert_meetup_event(meetup_event)

    def delete_unknown_events(self, event_ids):
        """Delete unknown (to Meetup) events given a set of event IDs."""
        for event_id in event_ids:
            xibo_event = self.xibo_events[event_id]
            action = self.anti_flapper.categorize(xibo_event)
            if action is not EventFlappingStatus.keep:
                self.xibo_event_crud.delete_xibo_event(
                        xibo_event, action.action)
                self.special_location_monitor.deleted_event(xibo_event)

    @staticmethod
    def event_list_to_dict(events):
        return {event.meetup_id: event for event in events}


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

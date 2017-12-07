"""Retrieve events from Meetup, extract data to display on signs, and
update the Xibo database."""

from config import MEETUP_API_CONFIG, LOCATION_CONFIG, XIBO_DB_CONFIG
from .meetup_api import MeetupEventsRetriever
from .location_extractor import LocationExtractor
from .event_converter import EventConverter, Event
from .logging_context import LoggingContext
from  .xibo_db import connect_to_xibo_db
import json
import logging


class Meetup2Xibo:

    """Downloads Meetup events into a Xibo databse."""

    def __init__(self, args):
        """Initialize with command line arguments."""
        self.args = args

    def main(self):

        with self.logging_context() as logger:
            self.logger = logger
#            json_events = self.retreive_meetup_json_events()
#            meetup_events = self.extract_events_from_json(json_events)
            meetup_events = []
            self.update_xibo_events(meetup_events)



    def logging_context(self):
        """Return a logging context."""
        log_level = logging.DEBUG if self.args.debug else logging.INFO
        logging_context =  LoggingContext(log_level = log_level, name = "meetup2xibo")
        logging_context.log_to_file(self.args.logfile)
        if self.args.verbose:
            logging_context.log_to_stderr()
        return logging_context

    def retreive_meetup_json_events(self):
        """Retrieve a list of Meetup events."""
        retriever = MeetupEventsRetriever(**MEETUP_API_CONFIG)
        json_events = retriever.retrieve_events_json()
        self.logger.info("JSON retrieved")
        return json_events

    def extract_events_from_json(self, json_events):
        """Extract event tuples from a list of Meetup JSON events."""
        location_extractor = LocationExtractor.from_location_phrases(**LOCATION_CONFIG)
        event_converter = EventConverter(location_extractor)
        meetup_events = {event_converter.convert(event_json) for event_json in json_events}
        self.logger.info("Events converted")
        return meetup_events

    def update_xibo_events(self, meetup_events):
        """Update events in the Xibo database with events downloaded from Meetup."""
        db_connection = connect_to_xibo_db(**XIBO_DB_CONFIG)
        new_event = Event("12345", "Joel's Birthday", "Kitchen", "2017-11-20 17:00:00", "2017-11-20 19:00:00")
        db_connection.insert_meetup_event(new_event)
        xibo_events = list(db_connection.get_xibo_events())
        for event in xibo_events:
            print(event)
#        db.connection.update_xibo(meetup_events, xibo_events)
        db_connection.delete_xibo_event(xibo_events[0])
        updated_event = Event("7890", "Debbie's Birthday", "Kitchen", "2017-09-11 17:00:00", "2017-09-11 19:00:00")
        db_connection.update_xibo_event(xibo_events[1], updated_event)


if __name__ == '__main__':

    from .command_line import parse_args

    args = parse_args()
    Meetup2Xibo(args).main()
            
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

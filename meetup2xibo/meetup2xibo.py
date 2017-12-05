"""Retrieve events from Meetup, extract data to display on signs, and
update the Xibo database."""

from config import MEETUP_API_CONFIG, LOCATION_CONFIG
from .meetup_api import MeetupEventsRetriever
from .location_extractor import LocationExtractor
from .event_converter import EventConverter
from .logging_context import LoggingContext, daily_file_handler, stderr_stream_handler
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
            json_events = self.retreive_meetup_json_events()
            meetup_events = self.extract_events_from_json(json_events)

            import csv
            with open("events.csv", 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(("meetup_id", "name", "start_time", "end_time", "location"))

                for event in meetup_events:
                    csv_writer.writerow(event)
                logger.info("CSV written")

    def logging_context(self):
        """Return a logging context."""
        file_handler = daily_file_handler(args.logfile)
        stderr_handler = stderr_stream_handler()
        log_level = logging.DEBUG if self.args.debug else logging.INFO
        return  LoggingContext(file_handler, stderr_handler, log_level = log_level, name = "meetup2xibo")

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


if __name__ == '__main__':

    from .command_line import parse_args

    args = parse_args()
    Meetup2Xibo(args).main()
            
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

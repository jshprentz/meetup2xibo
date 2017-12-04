"""Retrieve events from Meetup, extract data to display on signs, and
update the Xibo database."""

from config import MEETUP_API_CONFIG, LOCATION_CONFIG, LOG_CONFIG
from .meetup_api import MeetupEventsRetriever
from .location_extractor import LocationExtractor
from .event_converter import EventConverter
from .logging_context import LoggingContext, daily_file_handler, stderr_stream_handler
import json

if __name__ == "__main__":

    file_handler = daily_file_handler(LOG_CONFIG["filename"])
    stderr_handler = stderr_stream_handler()
    logging_context = LoggingContext(file_handler, stderr_handler, log_level = LOG_CONFIG["log_level"], name = "meetup2xibo")
    with logging_context as logger:

        retriever = MeetupEventsRetriever(**MEETUP_API_CONFIG)
        json_events = retriever.retrieve_events_json()
        logger.info("JSON retrieved")

        location_extractor = LocationExtractor.from_location_phrases(**LOCATION_CONFIG)
        event_converter = EventConverter(location_extractor)
        meetup_events = {event_converter.convert(event_json) for event_json in json_events}
        logger.info("Events converted")

        import csv
        with open("events.csv", 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(("meetup_id", "name", "start_time", "end_time", "location"))

            for event in meetup_events:
                csv_writer.writerow(event)
        logger.info("CSV written")
            
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

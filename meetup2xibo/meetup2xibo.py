"""Retrieve events from Meetup, extract data to display on signs, and
update the Xibo database."""

from config import MEETUP_API_CONFIG, LOCATION_CONFIG
from .meetup_api import MeetupEventsRetriever
from .location_extractor import LocationExtractor
from .event_converter import EventConverter
import json

if __name__ == "__main__":

    retriever = MeetupEventsRetriever(**MEETUP_API_CONFIG)
    json_events = retriever.retrieve_events_json()

    location_extractor = LocationExtractor.from_location_phrases(**LOCATION_CONFIG)
    event_converter = EventConverter(location_extractor)

    import csv
    with open("events.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(("meetup_id", "name", "start_time", "end_time", "location"))

        for event_json in json_events:
            event = event_converter.convert(event_json)
            csv_writer.writerow(event)
            
	
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

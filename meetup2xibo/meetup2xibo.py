"""Retrieve events from Meetup, extract data to display on signs, and
update the Xibo database."""

from config import MEETUP_API_CONFIG 
from .meetup_api import MeetupEventsRetriever
import json

if __name__ == "__main__":

    retriever = MeetupEventsRetriever(**MEETUP_API_CONFIG)
    json_events = retriever.retrieve_events_json()

    import csv
    with open("locations.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(("Venue Name", "Find Us"))

        for event_json in json_events:
            venue = event_json.get("venue", {"name": ""})
            name = venue["name"]
            find_us = event_json.get("how_to_find_us", "")
            csv_writer.writerow((name, find_us))
            if not name:
                print(event_json.get("name"))
	
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

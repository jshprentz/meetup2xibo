"""Retrieve events from Meetup, extract data to display on signs, and
update the Xibo database."""

from config import MEETUP_API_CONFIG 
from .meetup_api import MeetupEventsRetriever
import json

if __name__ == "__main__":

    retriever = MeetupEventsRetriever(**MEETUP_API_CONFIG)
    json_events = retriever.retrieve_events_json()
    print(json.dumps(json_events, sort_keys=True, indent=4))
    
    

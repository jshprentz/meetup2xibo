"""Tests for Meetup API"""

from .context import meetup2xibo
from meetup2xibo.meetup_api import MeetupEventsRetriever
import os
import json


def save_json(the_json, path):
    """Save JSON to a file."""
    pretty_json = json.dumps(the_json, indent = 4, sort_keys = True)
    with path.with_suffix(".json").open("w") as f:
        print(pretty_json, file = f)

def test_build_url():
    """Test building a URL."""
    retriever = MeetupEventsRetriever("foo_name", "bar_key")
    assert retriever.build_url() == "https://api.meetup.com/foo_name/events"

def test_request_params():
    """Test building a request parameter dictionary."""
    retriever = MeetupEventsRetriever("foo_name", "bar_key")
    expected_params = {
            "key": "bar_key",
            "scroll": "recent_past"
            }
    assert retriever.request_params() == expected_params

def test_cancelled_event_response(module_file_path):
    """Save response from an cancelled event request to Meetup."""
    group_name = os.getenv("MEETUP_GROUP_URL_NAME")
    api_key = os.getenv("MEETUP_API_KEY")
    retriever = MeetupEventsRetriever(group_name, api_key)
    response_json = retriever.retrieve_cancelled_events_json()
    save_json(response_json, module_file_path)



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

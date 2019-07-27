"""Tests for Meetup API"""

from meetup2xibo.updater.meetup_api import MeetupEventsRetriever
from datetime import datetime
import os
import json
import pytest


MEETUP_EVENTS_WANTED = 199


@pytest.fixture()
def meetup_event_retriever():
    """Return a Meetup events retriever configured to connect to Meetup.com."""
    group_name = os.getenv("MEETUP_GROUP_URL_NAME")
    last_time = os.getenv("NEAR_FUTURE_DATE")
    return MeetupEventsRetriever(group_name, MEETUP_EVENTS_WANTED, last_time)

def save_json(the_json, path):
    """Save JSON to a file."""
    pretty_json = json.dumps(the_json, indent = 4, sort_keys = True)
    with path.with_suffix(".json").open("w") as f:
        print(pretty_json, file = f)

def test_build_url():
    """Test building a URL."""
    retriever = MeetupEventsRetriever("foo_name", MEETUP_EVENTS_WANTED, None)
    assert retriever.build_url() == "https://api.meetup.com/foo_name/events"

def test_request_params():
    """Test building a request parameter dictionary."""
    retriever = MeetupEventsRetriever("foo_name", MEETUP_EVENTS_WANTED, None)
    expected_params = {
            "page": MEETUP_EVENTS_WANTED,
            "scroll": "recent_past"
            }
    assert retriever.request_params() == expected_params

def test_events_response(module_file_path, meetup_event_retriever):
    """Save response from an events request to Meetup."""
    response_json = meetup_event_retriever.retrieve_events_json()
    save_json(response_json, module_file_path)

def test_cancelled_events_response(module_file_path, meetup_event_retriever):
    """Save response from a cancelled events request to Meetup."""
    response_json = meetup_event_retriever.retrieve_cancelled_events_json()
    save_json(response_json, module_file_path)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

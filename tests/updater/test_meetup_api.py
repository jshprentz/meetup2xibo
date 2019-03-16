"""Tests for Meetup API"""

from ..context import meetup2xibo
from meetup2xibo.updater.meetup_api import MeetupEventsRetriever, meetup_iso_offset_time
from datetime import datetime
import os
import json
import pytest


MEETUP_EVENTS_WANTED = 199


@pytest.fixture()
def meetup_event_retriever():
    """Return a Meetup events retriever configured to connect to Meetup.com."""
    group_name = os.getenv("MEETUP_GROUP_URL_NAME")
    api_key = os.getenv("MEETUP_API_KEY")
    last_time = os.getenv("NEAR_FUTURE_DATE")
    return MeetupEventsRetriever(group_name, api_key, MEETUP_EVENTS_WANTED, last_time)

def save_json(the_json, path):
    """Save JSON to a file."""
    pretty_json = json.dumps(the_json, indent = 4, sort_keys = True)
    with path.with_suffix(".json").open("w") as f:
        print(pretty_json, file = f)

def test_build_url():
    """Test building a URL."""
    retriever = MeetupEventsRetriever("foo_name", "bar_key", MEETUP_EVENTS_WANTED, None)
    assert retriever.build_url() == "https://api.meetup.com/foo_name/events"

def test_request_params():
    """Test building a request parameter dictionary."""
    retriever = MeetupEventsRetriever("foo_name", "bar_key", MEETUP_EVENTS_WANTED, None)
    expected_params = {
            "key": "bar_key",
            "page": MEETUP_EVENTS_WANTED,
            "scroll": "recent_past"
            }
    assert retriever.request_params() == expected_params

def test_cancelled_event_response(module_file_path, meetup_event_retriever):
    """Save response from an cancelled event request to Meetup."""
    response_json = meetup_event_retriever.retrieve_cancelled_events_json()
    save_json(response_json, module_file_path)

def test_meetup_iso_offset_time():
    """Test formatting a future time."""
    now = datetime(2019, 3, 13, 15, 45, 22)
    future_seconds = 3601
    iso_time = meetup_iso_offset_time(now, future_seconds)
    assert iso_time == "2019-03-13T16:45:23.000"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

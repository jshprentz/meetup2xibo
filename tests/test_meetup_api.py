"""Tests for Meetup API"""

from .context import meetup2xibo
from meetup2xibo.meetup_api import MeetupEventsRetriever


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




# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

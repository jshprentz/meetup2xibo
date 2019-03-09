"""Access Meetup API to download events."""

from datetime import timedelta
import requests


class MeetupEventsRetriever:

    def __init__(self, group_url_name, api_key, cancelled_last_time):
        """Initialize with a Meetup group URL name, a Meetup API, and the last
        time allowed for cancelled events."""
        self.group_url_name = group_url_name
        self.api_key = api_key
        self.cancelled_last_time = cancelled_last_time

    def retrieve_events_json(self, **kwargs):
        """Retrieve the JSON event list, adding keyword arguments to the usual
        request parameters."""
        url = self.build_url()
        params = self.request_params()
        params.update(kwargs)
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def retrieve_cancelled_events_json(self, **kwargs):
        """Retrieve the JSON cancelled event list, adding keyword arguments to
        the usual request parameters."""
        return self.retrieve_events_json(
            status="cancelled",
            no_later_than=self.cancelled_last_time,
            **kwargs)

    def build_url(self):
        """Build a Meetup API URL to download events."""
        return "https://api.meetup.com/{}/events".format(self.group_url_name)

    def request_params(self):
        """Return a dictionary of request parameters."""
        return {
            "key": self.api_key,
            "scroll": "recent_past"
            }


def meetup_iso_offset_time(now, future_seconds):
    """Given a date/time, now, and an offset into the future in seconds,
    computer and return the resulting date/time formatted in ISO
    YYYY-MM-DDThh:mm:ss.000 format, as required by the Meetup API."""
    offset = timedelta(seconds=future_seconds)
    return (now + offset).strftime('%Y-%m-%dT%H:%M:%S.000')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

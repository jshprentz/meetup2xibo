"""Access Meetup API to download events."""

import requests


class MeetupEventsRetriever:

    def __init__(self, group_url_name, api_key):
        """Initialize with a Meetup group URL name and a
        Meetup API."""
        self.group_url_name = group_url_name
        self.api_key = api_key

    def retrieve_events_json(self, **kwargs):
        """Retrieve the JSON event list, adding keyword arguments to the usual
        request parameters."""
        url = self.build_url()
        params = self.request_params()
        params.update(kwargs)
        response = requests.get(url, params = params)
        response.raise_for_status()
        return response.json()

    def retrieve_cancelled_events_json(self, **kwargs):
        """Retrieve the JSON cancelled event list, adding keyword arguments to
        the usual request parameters."""
        return self.retrieve_events_json(status = "cancelled", **kwargs)

    def build_url(self):
        """Build a Meetup API URL to download events."""
        return "https://api.meetup.com/{}/events".format(self.group_url_name)

    def request_params(self):
        """Return a dictionary of request parameters."""
        return {
            "key": self.api_key,
            "scroll": "recent_past"
            }

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

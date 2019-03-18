"""Avoids flapping Xibo events."""

from datetime import timedelta
from enum import Enum


class EventFlappingStatus(Enum):

    """An event's status chosen by the anti-flapper."""

    Delete = 1
    Retire = 2
    Keep = 3


class AntiFlapper:

    """Avoids flapping caused when Xibo events do not match Meetup events.

    Meetup sometimes fails to retrieve current and recent events that should
    still be displayed.  Meetup often fails to retrieve far future events
    previously seen because newer events have been added with earlier meeting
    times.  Configuration specifies flapping windows around the current time
    and in the far future.  Missing meetup events will not be deleted from Xibo
    when they fall within the flapping windows."""

    def __init__(self, recent_limit, current_limit, future_limit):
        """Initialize with flapping window limits in the ISO format used by
        Xibo: YYYY-MM-DD hh:mm:ss. The flapping windows fall between the recent
        and current limit and after the future limit."""
        self.recent_limit = recent_limit
        self.current_limit = current_limit
        self.future_limit = future_limit

    def categorize(self, xibo_event):
        """Categorize an event based on its times and the flapping window.
        Return an event flapping status."""
        if self.is_future(xibo_event):
            return EventFlappingStatus.Keep
        elif self.is_past(xibo_event):
            return EventFlappingStatus.Retire
        elif self.is_planned(xibo_event):
            return EventFlappingStatus.Delete
        else:
            return EventFlappingStatus.Keep
                
    def is_past(self, xibo_event):
        """ Return true if the event ends before the anti-flapping window;
        false otherwise. """
        return xibo_event.end_time < self.recent_limit

    def is_planned(self, xibo_event):
        """ Return true if the event is planned between the two flapping
        windows; false otherwise. """
        return xibo_event.start_time > self.current_limit

    def is_future(self, xibo_event):
        """ Return true if the event ends after the future limit; false
        otherwise. """
        return xibo_event.end_time > self.future_limit


def iso_offset_time(now, future_seconds):
    """Given a date/time, now, and an offset into the future
    in seconds, computer and return the resulting date/time
    formatted in ISO YYYY-MM-DD hh:mm:ss format."""
    offset = timedelta(seconds=future_seconds)
    return (now + offset).strftime('%Y-%m-%d %H:%M:%S')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

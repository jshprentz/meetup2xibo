"""Avoids flapping Xibo events."""

from datetime import timedelta


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

    def is_ok(self, xibo_event):
        """Test whether a Xibo event falls outside the flapping windows."""
        is_past = xibo_event.end_time < self.recent_limit
        is_planned = xibo_event.start_time > self.current_limit
        is_future = xibo_event.end_time > self.future_limit 
        return (is_past or is_planned) and not is_future

def iso_offset_time(now, future_seconds):
    """Given a date/time, now, and an offset into the future
    in seconds, computer and return the resulting date/time
    formatted in ISO YYYY-MM-DD hh:mm:ss format."""
    offset = timedelta(seconds = future_seconds)
    return (now + offset).strftime('%Y-%m-%d %H:%M:%S')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

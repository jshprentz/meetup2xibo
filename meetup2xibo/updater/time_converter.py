"""Converts times from Meetup to Xibo formats.

The Meetup API reports event dates and times in POSIX epoch milliseconds since
January 1, 1970, effectively UTC date/times. The Meetup API expects times in
ISO 8601 YYYY-MM-DDThh:mm:ss.000 format.

Xibo stores event date/times as strings in ISO 8601 ISO YYYY-MM-DD hh:mm:ss
format. The Xibo CMS expects date/times converted to the local timezone
configured in the CMS.
"""

from datetime import datetime, timedelta


def meetup_time_format(a_datetime):
    """Format a date/time for Meetup."""
    return a_datetime.strftime('%Y-%m-%dT%H:%M:%S.000')


def xibo_time_format(a_datetime):
    """Format a date/time for Xibo."""
    return a_datetime.strftime('%Y-%m-%d %H:%M:%S')


def offset_time(now, future_seconds):
    """Given a date/time, now, and an offset into the future
    in seconds, compute and return the resulting date/time."""
    offset = timedelta(seconds=future_seconds)
    return now + offset


class DateTimeCreator:

    """A timezone aware date/time creator."""

    def __init__(self, tzinfo):
        """Initialize with Python timezone info for Xibo's configured local
        time."""
        self.tzinfo = tzinfo

    def now(self):
        """Return the current date and time in the configured timezone."""
        return datetime.now(self.tzinfo)

    def from_epoch_ms(self, epoch_ms):
        """Return the date and time corresponding to the POSIX timestamp (in
        milliseconds) in the configured timezone."""
        return datetime.fromtimestamp(epoch_ms/1000, self.tzinfo)

    def xibo_time(self, epoch_ms):
        """Format a time represented as milliseconds since the Unix epoch
        in ISO YYYY-MM-DD hh:mm:ss format."""
        return xibo_time_format(self.from_epoch_ms(epoch_ms))

    def xibo_offset_time(self, future_seconds):
        """Given a date/time, now, and an offset into the future
        in seconds, computer and return the resulting date/time
        formatted in ISO YYYY-MM-DD hh:mm:ss format."""
        return xibo_time_format(offset_time(self.now(), future_seconds))

    def meetup_offset_time(self, future_seconds):
        """Given a date/time, now, and an offset into the future in seconds,
        computer and return the resulting date/time formatted in ISO
        YYYY-MM-DDThh:mm:ss.000 format, as required by the Meetup API."""
        return meetup_time_format(offset_time(self.now(), future_seconds))


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Test the Meetup to Xibo time converter."""

from meetup2xibo.updater.time_converter import DateTimeCreator, \
    meetup_time_format, xibo_time_format, offset_time
from datetime import datetime
from pytz import timezone
import pytest
from freezegun import freeze_time


# Winter: London and New York use standard time.
WINTER_EPOCH_MS = 1546191000000
WINTER_MEETUP_TIME_LONDON = "2018-12-30T17:30:00.000"
WINTER_MEETUP_TIME_NEW_YORK = "2018-12-30T12:30:00.000"
WINTER_XIBO_TIME_LONDON = "2018-12-30 17:30:00"
WINTER_XIBO_TIME_NEW_YORK = "2018-12-30 12:30:00"

# Early Spring: London uses standard time; New York uses daylight savings time.
SPRING_EPOCH_MS = 1553091072000
SPRING_MEETUP_TIME_LONDON = "2019-03-20T14:11:12.000"
SPRING_MEETUP_TIME_NEW_YORK = "2019-03-20T10:11:12.000"
SPRING_XIBO_TIME_LONDON = "2019-03-20 14:11:12"
SPRING_XIBO_TIME_NEW_YORK = "2019-03-20 10:11:12"

# Summer: London and New York use daylight savings time.
SUMMER_EPOCH_MS = 1565788500123
SUMMER_MEETUP_TIME_LONDON = "2019-08-14T14:15:00.000"
SUMMER_MEETUP_TIME_NEW_YORK = "2019-08-14T09:15:00.000"
SUMMER_XIBO_TIME_LONDON = "2019-08-14 14:15:00"
SUMMER_XIBO_TIME_NEW_YORK = "2019-08-14 09:15:00"


@pytest.fixture
def new_york_timezone():
    """Return the timezone info for New York City (EST/EDT)."""
    return timezone('America/New_York')

@pytest.fixture
def london_timezone():
    """Return the timezone info for London (GMT/BST)."""
    return timezone('Europe/London')

@pytest.fixture
def new_york_datetime_creator(new_york_timezone):
    """Return a date/time creator configured for the New York timezone."""
    return DateTimeCreator(new_york_timezone)

@pytest.fixture
def london_datetime_creator(london_timezone):
    """Return a date/time creator configured for the London timezone."""
    return DateTimeCreator(london_timezone)

@freeze_time(SUMMER_XIBO_TIME_LONDON, tz_offset=-1)
def test_now_london(london_datetime_creator):
    """Test returning the current (frozen) date and time in London."""
    xibo_formatted_now = xibo_time_format(london_datetime_creator.now())
    assert SUMMER_XIBO_TIME_LONDON == xibo_formatted_now

@freeze_time(WINTER_XIBO_TIME_NEW_YORK, tz_offset=5)
def test_now_new_york(new_york_datetime_creator):
    """Test returning the current (frozen) date and time in New York."""
    xibo_formatted_now = xibo_time_format(new_york_datetime_creator.now())
    assert WINTER_XIBO_TIME_NEW_YORK == xibo_formatted_now

@pytest.mark.parametrize("epoch_ms,expected_formatted_time", [
    (WINTER_EPOCH_MS, WINTER_MEETUP_TIME_LONDON),
    (SPRING_EPOCH_MS, SPRING_MEETUP_TIME_LONDON),
    (SUMMER_EPOCH_MS, SUMMER_MEETUP_TIME_LONDON),
    ])
def test_meetup_time_format_london(epoch_ms, expected_formatted_time, london_datetime_creator):
    """Test creating date/times in London and formatting them for the Meetup API."""
    a_datetime = london_datetime_creator.from_epoch_ms(epoch_ms)
    assert expected_formatted_time == meetup_time_format(a_datetime)

@pytest.mark.parametrize("epoch_ms,expected_formatted_time", [
    (WINTER_EPOCH_MS, WINTER_MEETUP_TIME_NEW_YORK),
    (SPRING_EPOCH_MS, SPRING_MEETUP_TIME_NEW_YORK),
    (SUMMER_EPOCH_MS, SUMMER_MEETUP_TIME_NEW_YORK),
    ])
def test_meetup_time_format_new_york(epoch_ms, expected_formatted_time, new_york_datetime_creator):
    """Test creating date/times in New York and formatting them for the Meetup API."""
    a_datetime = new_york_datetime_creator.from_epoch_ms(epoch_ms)
    assert expected_formatted_time == meetup_time_format(a_datetime)

@pytest.mark.parametrize("epoch_ms,expected_formatted_time", [
    (WINTER_EPOCH_MS, WINTER_XIBO_TIME_LONDON),
    (SPRING_EPOCH_MS, SPRING_XIBO_TIME_LONDON),
    (SUMMER_EPOCH_MS, SUMMER_XIBO_TIME_LONDON),
    ])
def test_xibo_time_format_london(epoch_ms, expected_formatted_time, london_datetime_creator):
    """Test creating date/times in London and formatting them for the Meetup API."""
    a_datetime = london_datetime_creator.from_epoch_ms(epoch_ms)
    assert expected_formatted_time == xibo_time_format(a_datetime)

@pytest.mark.parametrize("epoch_ms,expected_formatted_time", [
    (WINTER_EPOCH_MS, WINTER_XIBO_TIME_NEW_YORK),
    (SPRING_EPOCH_MS, SPRING_XIBO_TIME_NEW_YORK),
    (SUMMER_EPOCH_MS, SUMMER_XIBO_TIME_NEW_YORK),
    ])
def test_xibo_time_format_new_york(epoch_ms, expected_formatted_time, new_york_datetime_creator):
    """Test creating date/times in New York and formatting them for the Meetup API."""
    a_datetime = new_york_datetime_creator.from_epoch_ms(epoch_ms)
    assert expected_formatted_time == xibo_time_format(a_datetime)

def test_iso_offset_time_future(new_york_datetime_creator):
    """Test offsetting time into the future."""
    now = new_york_datetime_creator.from_epoch_ms(WINTER_EPOCH_MS)
    future_time = offset_time(now, 4500)
    assert "2018-12-30 13:45:00" == xibo_time_format(future_time)

def test_xibo_time(new_york_datetime_creator):
    """Test converting epoch milliseconds into a date/time formatted for Xibo."""
    xibo_time = new_york_datetime_creator.xibo_time(SPRING_EPOCH_MS)
    assert SPRING_XIBO_TIME_NEW_YORK == xibo_time

@freeze_time(WINTER_XIBO_TIME_NEW_YORK, tz_offset=5)
def test_xibo_offset_time(new_york_datetime_creator):
    """Test offsetting the current time into the future and formatting it for Xibo."""
    offset_time = new_york_datetime_creator.xibo_offset_time(4500)
    assert "2018-12-30 13:45:00" == offset_time

@freeze_time(WINTER_XIBO_TIME_NEW_YORK, tz_offset=5)
def test_meetup_offset_time(new_york_datetime_creator):
    """Test offsetting the current time into the future and formatting it for Meetup."""
    offset_time = new_york_datetime_creator.meetup_offset_time(4500)
    assert "2018-12-30T13:45:00.000" == offset_time

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

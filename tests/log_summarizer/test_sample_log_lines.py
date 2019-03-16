"""Test providing sample log lines."""

import pytest

def test_date_time(sample_log_lines):
    """Test getting a date/time."""
    line = sample_log_lines.date_time()
    assert line == "2019-03-04 06:00:12"

def test_start_line(sample_log_lines):
    """Test getting a start line."""
    line = sample_log_lines.start_line()
    assert line == "2019-03-04 06:00:53,454 - INFO - meetup2xibo - Start meetup2xibo 2.0.1"

def test_start_line_second(sample_log_lines):
    """Test incremented time in second start line."""
    line1 = sample_log_lines.start_line()
    line2 = sample_log_lines.start_line()
    assert line2 == "2019-03-04 06:01:53,454 - INFO - meetup2xibo - Start meetup2xibo 2.0.1"

def test_end_line(sample_log_lines):
    """Test getting an end line."""
    line = sample_log_lines.end_line()
    assert line == "2019-03-04 06:00:14,566 - INFO - meetup2xibo - End meetup2xibo 2.0.1"

def test_insert_line(sample_log_lines):
    """Test getting an insert line."""
    line = sample_log_lines.insert_line()
    assert line.startswith("2019-03-04 06:00:12,865 - INFO - XiboEventCrud - Inserted Event")

def test_update_line(sample_log_lines):
    """Test getting an update line."""
    line = sample_log_lines.update_line()
    assert line.startswith("2019-03-04 06:00:59,273 - INFO - XiboEventCrud - Updated from ")
    assert "\n2019-03-04 06:00:59,274 - INFO - XiboEventCrud - Updated to " in line

def test_delete_line(sample_log_lines):
    """Test getting a delete line."""
    line = sample_log_lines.delete_line()
    assert line.startswith("2019-03-04 06:00:57,083 - INFO - XiboEventCrud - Deleted ")

def test_unknown_location_line(sample_log_lines):
    """Test getting an unknown_location line."""
    line = sample_log_lines.unknown_location_line()
    assert line.startswith(
        "2019-03-04 06:00:11,441 - WARNING - LocationChooser - " 
        "Unknown location for PartialEvent")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

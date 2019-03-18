"""Test collecting mappings from venue/find-us to location."""

from meetup2xibo.log_summarizer.location_mapper import LocationMapper
import pytest

@pytest.fixture
def location_mapper():
    """Return a location mapper."""
    return LocationMapper()

def test_has_mappings_none(location_mapper):
    """Test that an empty location mapper does not have mappings."""
    assert not location_mapper.has_mappings()

def test_has_mappings_one(location_mapper, sample_log_lines):
    """Test that a location mapper with one mapping has mappings."""
    log_line = sample_log_lines.make_event_location_log_line()
    location_mapper.add_event_location_log_line(log_line)
    assert location_mapper.has_mappings()

def test_mapping_list_identical(location_mapper, sample_log_lines):
    """Test that the mapping list contains only one copy of identical mappings."""
    log_line_1 = sample_log_lines.make_event_location_log_line()
    log_line_2 = sample_log_lines.make_event_location_log_line()
    location_mapper.add_event_location_log_line(log_line_1)
    location_mapper.add_event_location_log_line(log_line_2)
    assert [log_line_2] == location_mapper.mapping_list()

def test_mapping_list_different(location_mapper, sample_log_lines):
    """Test that the mapping list contains a copy of each different mapping."""
    log_line_1 = sample_log_lines.make_event_location_log_line("Metal Shop")
    log_line_2 = sample_log_lines.make_event_location_log_line("Wood Shop")
    location_mapper.add_event_location_log_line(log_line_1)
    location_mapper.add_event_location_log_line(log_line_2)
    assert [log_line_1, log_line_2] == location_mapper.mapping_list()

def test_mapping_list_sorted(location_mapper, sample_log_lines):
    """Test that the mapping list is sorted."""
    log_line_1 = sample_log_lines.make_event_location_log_line("Metal Shop")
    log_line_2 = sample_log_lines.make_event_location_log_line("Wood Shop")
    log_line_3 = sample_log_lines.make_event_location_log_line("Conference Room 3")
    log_line_4 = sample_log_lines.make_event_location_log_line("Classroom A")
    location_mapper.add_event_location_log_line(log_line_1)
    location_mapper.add_event_location_log_line(log_line_2)
    location_mapper.add_event_location_log_line(log_line_3)
    location_mapper.add_event_location_log_line(log_line_4)
    assert [log_line_4, log_line_3, log_line_1, log_line_2] == location_mapper.mapping_list()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent


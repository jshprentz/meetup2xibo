"""Test rendering mappings from venue/find-us to location."""

from meetup2xibo.log_summarizer.location_mapper import LocationMapper
from meetup2xibo.log_summarizer.renderer import LocationMappingCsvRenderer
import pytest

EXPECTED_HEADER = 'Location,Venue,Find Us,Example Meetup,Example URL\r\n'

EXPECTED_CSV_1 = 'Woodshop,Nova Labs (Woodshop),[Woodshop Red area],' \
        'Customized Wooden Beer Caddy,https://www.meetup.com/NOVA-Makers/events/259405866/\r\n'

@pytest.fixture
def location_mapper():
    """Return a location mapper."""
    return LocationMapper()

@pytest.fixture
def csv_renderer():
    """Return a location mapping CSV renderer."""
    return LocationMappingCsvRenderer()

def test_render_none(location_mapper, csv_renderer):
    """Test rendering an empty string when there are no location mappings."""
    assert "" == csv_renderer.render(location_mapper)

def test_render_one(location_mapper, csv_renderer, sample_log_lines):
    """Test rendering one mapping as comma separated values."""
    log_line_1 = sample_log_lines.make_event_location_log_line()
    location_mapper.add_event_location_log_line(log_line_1)
    expected_csv = EXPECTED_HEADER + EXPECTED_CSV_1
    assert expected_csv == csv_renderer.render(location_mapper)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent


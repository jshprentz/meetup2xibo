"""Test an email renderer."""

from meetup2xibo.log_summarizer.renderer import EmailRenderer
from email.headerregistry import Address
import pytest

SAMPLE_TO_ADDRESS = "smith@example.com"

EXPECTED_EMAIL_HEADER = """Subject: The subject
To: smith@example.com
"""

EXPECTED_HTML_ONLY_HEADER = """Content-Type: text/html; charset="utf-8"
Content-Transfer-Encoding: 7bit
MIME-Version: 1.0
"""

EXPECTED_MULTIPART_HEADER = """MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="======"""

EXPECTED_HTML_PART_HEADER = """Content-Type: text/html; charset="utf-8"
Content-Transfer-Encoding: 7bit

"""

EXPECTED_CSV_PART_HEADER = """Content-Type: text/csv; charset="utf-8"
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="meetup_locations.csv"
MIME-Version: 1.0

"""


SAMPLE_HTML = "<!-- sample -->\n"

SAMPLE_CSV = "Name,Address,Zip\n"


def test_can_render_no():
    """Test that an email renderer cannnot render without a "To" address."""
    email_renderer = EmailRenderer("", "The subject")
    assert not email_renderer.can_render()

def test_can_render_yes():
    """Test that an email renderer can render with a "To" address."""
    email_renderer = EmailRenderer(SAMPLE_TO_ADDRESS, "")
    assert email_renderer.can_render()

def test_address_list_one():
    """Test making an address list with one address."""
    email_renderer = EmailRenderer(SAMPLE_TO_ADDRESS, "")
    expected_address_1 = Address(username='smith', domain='example.com')
    assert email_renderer.address_list() == (expected_address_1, )

def test_address_list_two():
    """Test making an address list with two addresses."""
    email_renderer = EmailRenderer(SAMPLE_TO_ADDRESS + " jones@foo.com", "")
    expected_address_1 = Address(username='smith', domain='example.com')
    expected_address_2 = Address(username='jones', domain='foo.com')
    assert email_renderer.address_list() == (expected_address_1, expected_address_2)

def test_make_message():
    """Test making an empty message with a "To" address and subject."""
    email_renderer = EmailRenderer(SAMPLE_TO_ADDRESS, "The subject")
    assert str(email_renderer.make_message()) == EXPECTED_EMAIL_HEADER + "\n"

def test_render_html():
    """Test rendering a message with some HTML."""
    email_renderer = EmailRenderer(SAMPLE_TO_ADDRESS, "The subject")
    expected_rendering= EXPECTED_EMAIL_HEADER + EXPECTED_HTML_ONLY_HEADER + "\n" + SAMPLE_HTML
    assert email_renderer.render(SAMPLE_HTML, None) == expected_rendering

def test_render_html_and_csv():
    """Test rendering a message with some HTML and attached CSV data."""
    email_renderer = EmailRenderer(SAMPLE_TO_ADDRESS, "The subject")
    expected_rendering= EXPECTED_EMAIL_HEADER + EXPECTED_HTML_ONLY_HEADER + "\n" + SAMPLE_HTML + SAMPLE_CSV
    rendering = email_renderer.render(SAMPLE_HTML, SAMPLE_CSV)
    print(repr(rendering))
    assert rendering.startswith(EXPECTED_EMAIL_HEADER + EXPECTED_MULTIPART_HEADER)
    assert (EXPECTED_CSV_PART_HEADER + SAMPLE_CSV) in rendering
    assert (EXPECTED_HTML_PART_HEADER + SAMPLE_HTML) in rendering


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

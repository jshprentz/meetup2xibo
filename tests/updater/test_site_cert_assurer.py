"""Test assuring that an site SSL certificate will be used."""

from meetup2xibo.updater.site_cert_assurer import SiteCertAssurer
import logging


GOOD_SSL_URL = "https://www.google.com/"
BAD_SSL_URL = "https://untrusted-root.badssl.com/"

EXPECTED_CERT_MESSAGE = """
# Site-specific certificate authority
# Site: https://example.com
# File: /site/ca/path
"""

EXPECTED_FILE_CONTENTS_FORMAT = """abc
# Site-specific certificate authority
# Site: https://example2.com
# File: {}
def"""

def test_cert_message():
    """Test the formatting of a certificate message."""
    assurer = SiteCertAssurer(
            sys_ca_path = "/sys/ca/path",
            site_ca_path = "/site/ca/path",
            site_url = "https://example.com",
            user_agent = "test/123")
    assert assurer.cert_message() == EXPECTED_CERT_MESSAGE

def test_file_append(tmpdir, caplog):
    """Test appending the site certificate authority to the certificate
    authority bundle."""
    caplog.set_level(logging.INFO)
    foo_path = tmpdir.join("foo")
    foo_path.write("abc")
    bar_path = tmpdir.join("bar")
    bar_path.write("def")
    assurer = SiteCertAssurer(
            sys_ca_path = str(foo_path),
            site_ca_path = str(bar_path),
            site_url = "https://example2.com",
            user_agent = "test/123")
    assurer.append_site_cert()
    assert foo_path.read() == EXPECTED_FILE_CONTENTS_FORMAT.format(bar_path)
    assert bar_path.read() == "def"

def test_have_valid_cert_good():
    """Test checking for a valid site certificate at
    a site with a good SSL certificate."""
    assurer = SiteCertAssurer(
            sys_ca_path = None,
            site_ca_path = None,
            site_url = GOOD_SSL_URL,
            user_agent = "test/123")
    assert assurer.have_valid_cert()

def test_have_valid_cert_bad():
    """Test checking for a valid site certificate at
    a site with a bad SSL certificate."""
    assurer = SiteCertAssurer(
            sys_ca_path = None,
            site_ca_path = None,
            site_url = BAD_SSL_URL,
            user_agent = "test/123")
    assert not assurer.have_valid_cert()

def test_assure_site_cert_known(mocker):
    """Test assuring a site certificate when it already is known."""
    assurer = SiteCertAssurer(
            sys_ca_path = None,
            site_ca_path = None,
            site_url = None,
            user_agent = "test/123")
    mocker.patch.object(assurer, "have_valid_cert", return_value = True)
    mocker.patch.object(assurer, "append_site_cert")
    assurer.assure_site_cert()
    assurer.append_site_cert.assert_not_called()

def test_assure_site_cert_unknown(mocker):
    """Test assuring a site certificate when it is unknown."""
    assurer = SiteCertAssurer(
            sys_ca_path = "/foo",
            site_ca_path = "/bar",
            site_url = "https://example.com",
            user_agent = "test/123")
    mocker.patch.object(assurer, "have_valid_cert", return_value = False)
    mocker.patch.object(assurer, "append_site_cert")
    assurer.assure_site_cert()
    assurer.append_site_cert.assert_called_once_with()



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

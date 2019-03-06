"""Assures that Python Requests recognizes a site's certificate."""

import requests
import certifi
import logging


class SiteCertAssurer(object):

    """Assures that Python Requests recognizes a site's certificate."""

    logger = logging.getLogger("SiteCertAssurer")

    def __init__(self, sys_ca_path, site_ca_path, site_url, user_agent):
        """Initialize with paths to the Python Requests certificate authority
        file and the site-specific certificate authority file (in PEM format),
        a site URL, and a user agent for HTTPS requests."""
        self.sys_ca_path = sys_ca_path
        self.site_ca_path = site_ca_path
        self.site_url = site_url
        self.user_agent = user_agent

    def assure_site_cert(self):
        """Assure that the site at URL has a valid SSL certificate we
        recognize."""
        if self.site_ca_path and self.site_url and self.sys_ca_path:
            if not self.have_valid_cert():
                self.append_site_cert()

    def have_valid_cert(self):
        """Check that we have a valid SSL certificate for the site URL."""
        try:
            headers = {'User-Agent': self.user_agent}
            requests.get(self.site_url, headers=headers)
            return True
        except requests.exceptions.SSLError:
            return False

    def cert_message(self):
        """Return a formatted message for the certificate authority file."""
        return """
# Site-specific certificate authority
# Site: {}
# File: {}
""".format(self.site_url, self.site_ca_path)

    def append_site_cert(self):
        """Append the site-specific certificate authority file to the Python
        Requests certificate authority file."""
        self.logger.info(
                "Appending site CA %s to system CA list %s",
                self.site_ca_path, self.sys_ca_path)
        with open(self.site_ca_path, 'rb') as site_ca_file:
            site_ca = site_ca_file.read()
        with open(self.sys_ca_path, 'ab') as sys_ca_file:
            sys_ca_file.write(self.cert_message().encode())
            sys_ca_file.write(site_ca)


def assure_site_cert(site_ca_path, site_url):
    """Assure that the site's certificate authority is available for accessing
    the URL."""
    if site_ca_path and site_url:
        sys_ca_path = certifi.where()
        assurer = SiteCertAssurer(
                sys_ca_path, site_ca_path, site_url, "test/456")
        assurer.assure_site_cert()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

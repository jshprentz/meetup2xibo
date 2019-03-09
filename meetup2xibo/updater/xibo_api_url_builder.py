"""Builds URLs for the XIBO API."""

from urllib.parse import urljoin


class XiboApiUrlBuilder:

    """Builds URLs for Xibo API methods."""

    def __init__(self, hostname, port=None):
        """Initialize with a hostname and port."""
        if port is None or port == '443' or port == 443:
            self.base_url = "https://{}".format(hostname)
        else:
            self.base_url = "https://{}:{}".format(hostname, port)

    def access_token_url(self):
        """Return the URL to access a token."""
        return urljoin(self.base_url, "/api/authorize/access_token")

    def about_url(self):
        """Return the URL for API version information."""
        return urljoin(self.base_url, "/api/about")

    def cert_validation_url(self):
        """Return the URL for validating certificates."""
        return self.base_url

    def dataset_url(self):
        """Return the URL for retrieving dataset metadata."""
        return urljoin(self.base_url, "/api/dataset")

    def dataset_column_url(self, dataset_id):
        """Return the URL for retrieving column descriptions from
        the specified dataset."""
        return urljoin(
                self.base_url,
                "/api/dataset/{}/column".format(dataset_id))

    def dataset_data_url(self, dataset_id):
        """Return the URL for data from the specified dataset."""
        return urljoin(
                self.base_url,
                "/api/dataset/data/{}".format(dataset_id))

    def dataset_data_row_url(self, dataset_id, row_id):
        """Return the URL for the specified row from
        the specified dataset."""
        return urljoin(
                self.base_url,
                "/api/dataset/data/{}/{}".format(dataset_id, row_id))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

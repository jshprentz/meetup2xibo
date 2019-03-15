"""Access Xibo API to update events."""


from .http_response_error import XiboApiError
from itertools import chain
import logging


class XiboApi:

    """Hides details of accessing the Xibo API."""

    logger = logging.getLogger("Xibo_API_Connection")

    def __init__(self, session, xibo_api_url_builder, page_length):
        """Initialize with an OAuth2 session to the Xibo server,
        a Xibo API URL builder, and a page length for paged retrievals."""
        self.session = session
        self.xibo_api_url_builder = xibo_api_url_builder
        self.page_length = page_length

    def get_response(self, url, **payload):
        """Request a URL and return the response."""
        response = self.session.get(url, params=payload)
        XiboApiError.check_response_status(response)
        return response

    def get_json(self, url, **payload):
        """Request a URL and return the JSON result."""
        response = self.get_response(url, **payload)
        return response.json()

    def get_json_pages(self, url, **payload):
        """Return a generator of JSON pages requested from the URL."""
        start = 0
        response = self.get_json(
                url, start=start, length=self.page_length, **payload)
        yield response
        while len(response) == self.page_length:
            start += self.page_length
            response = self.get_json(
                    url, start=start, length=self.page_length, **payload)
            yield response

    def get_paged_json(self, url, **payload):
        """Request a URL and return an iterable of all paged JSON results."""
        json_pages = self.get_json_pages(url, **payload)
        return chain.from_iterable(json_pages)

    def delete(self, url, **payload):
        """Request deletion at a URL and return the response."""
        response = self.session.delete(url, params=payload)
        XiboApiError.check_response_status(response)
        return response

    def post(self, url, **payload):
        """Request posting at a URL and return the response."""
        response = self.session.post(url, data=payload)
        XiboApiError.check_response_status(response)
        return response

    def put(self, url, **payload):
        """Request puting at a URL and return the response."""
        response = self.session.put(url, data=payload)
        XiboApiError.check_response_status(response)
        return response

    def get_about(self):
        """Get the JSON representing the Xibo API version and
        other "about" information."""
        url = self.xibo_api_url_builder.about_url()
        return self.get_json(url)

    def get_xibo_api_version(self):
        """Return the Xibo API version string."""
        return self.get_about()["version"]

    def get_datasets_by_code(self, dataset_code):
        """Get a JSON list of metadata about a dataset,
        searching by its code."""
        url = self.xibo_api_url_builder.dataset_url()
        return self.get_json(url, code=dataset_code)

    def get_dataset_column_by_id(self, dataset_id):
        """Get a JSON list of dataset column metadata,
        searching by the dataset id."""
        url = self.xibo_api_url_builder.dataset_column_url(dataset_id)
        return self.get_paged_json(url)

    def get_dataset_data_by_id(self, dataset_id):
        """Get a JSON list of dataset data,
        searching by its id."""
        url = self.xibo_api_url_builder.dataset_data_url(dataset_id)
        return self.get_paged_json(url)

    def delete_dataset_data_by_id(self, dataset_id, row_id):
        """Delete the dataset row."""
        url = self.xibo_api_url_builder.dataset_data_row_url(
                dataset_id, row_id)
        return self.delete(url)

    def insert_dataset_data(self, dataset_id, columns):
        """Insert a row of data into the Xibo database."""
        url = self.xibo_api_url_builder.dataset_data_url(dataset_id)
        return self.post(url, **columns)

    def update_dataset_data(self, dataset_id, row_id, columns):
        """Update a row of data in the Xibo database."""
        url = self.xibo_api_url_builder.dataset_data_row_url(
                dataset_id, row_id)
        return self.put(url, **columns)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

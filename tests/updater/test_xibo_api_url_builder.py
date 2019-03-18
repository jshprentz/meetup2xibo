"""Test generating Xibo API URLs."""

from meetup2xibo.updater.xibo_api_url_builder import XiboApiUrlBuilder


def test_access_token_url_default_port():
    """Test generating the URL for an OAuth2 token."""
    url_builder = XiboApiUrlBuilder("example1.com")
    expected_url = "https://example1.com/api/authorize/access_token"
    assert expected_url == url_builder.access_token_url()

def test_access_token_url_with_explicit_port_443():
    """Test generating the URL for an OAuth2 token."""
    url_builder = XiboApiUrlBuilder("example2.com")
    expected_url = "https://example2.com/api/authorize/access_token"
    assert expected_url == url_builder.access_token_url()

def test_access_token_url_with_other_port():
    """Test generating the URL for an OAuth2 token."""
    url_builder = XiboApiUrlBuilder("example3.com", 8080)
    expected_url = "https://example3.com:8080/api/authorize/access_token"
    assert expected_url == url_builder.access_token_url()

def test_about_url():
    """Test generating the URL for an "about" request."""
    url_builder = XiboApiUrlBuilder("example4.com")
    expected_url = "https://example4.com/api/about"
    assert expected_url == url_builder.about_url()

def test_cert_validation_url():
    """Test generating the URL for validating a certificate."""
    url_builder = XiboApiUrlBuilder("example5.com")
    expected_url = "https://example5.com"
    assert expected_url == url_builder.cert_validation_url()

def test_dataset_url():
    """Test generating the URL for a "dataset" request."""
    url_builder = XiboApiUrlBuilder("example6.com")
    expected_url = "https://example6.com/api/dataset"
    assert expected_url == url_builder.dataset_url()

def test_dataset_column_url():
    """Test generating the URL for a "dataset column" request."""
    url_builder = XiboApiUrlBuilder("example8.com")
    expected_url = "https://example8.com/api/dataset/234/column"
    assert expected_url == url_builder.dataset_column_url(234)

def test_dataset_data_url():
    """Test generating the URL for a "dataset data" request."""
    url_builder = XiboApiUrlBuilder("example7.com")
    expected_url = "https://example7.com/api/dataset/data/123"
    assert expected_url == url_builder.dataset_data_url(123)

def test_dataset_data_row_url():
    """Test generating the URL for deleting or editing a dataset row."""
    url_builder = XiboApiUrlBuilder("example9.com")
    expected_url = "https://example9.com/api/dataset/data/123/456"
    assert expected_url == url_builder.dataset_data_row_url(123, 456)



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

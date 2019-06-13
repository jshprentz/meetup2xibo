"""Test generating the Xibo API."""

from meetup2xibo.updater.xibo_api import XiboApi
from meetup2xibo.updater.xibo_event import XiboEvent
from meetup2xibo.updater.http_response_error import XiboApiError
from requests_toolbelt.utils import dump
import json
import os
import pytest

SAMPLE_URL = "https://example.com/api"

SAMPLE_XIBO_EVENT_COLUMNS = {
    'dataSetColumnId_1': "Nova Labs Open House",
    'dataSetColumnId_2': "Orange Bay",
    'dataSetColumnId_3': "zvbxrpl2",
    'dataSetColumnId_4': "2019-02-26 15:00:00",
    'dataSetColumnId_5': "2019-02-26 17:00:00"
}

SAMPLE_ABOUT_JSON = json.loads("""{
    "sourceUrl": null,
    "version": "1.8.12"
}""")

SAMPLE_JSON_LIST_0 = json.loads("[]")
SAMPLE_JSON_LIST_1 = json.loads("[111]")
SAMPLE_JSON_LIST_2 = json.loads("[211, 222]")
SAMPLE_JSON_LIST_3 = json.loads("[311, 322, 333]")

SAMPLE_XIBO_PAGE_LENGTH = 3
REAL_XIBO_PAGE_LENGTH = 50


def save_json(the_json, path):
    """Save JSON to a file."""
    pretty_json = json.dumps(the_json, indent = 4, sort_keys = True)
    with path.with_suffix(".json").open("w") as f:
        print(pretty_json, file = f)

def save_response(response, path):
    """Save an HTTP response to the path."""
    with path.with_suffix(".txt").open("w") as f:
        data = dump.dump_response(response)
        print(data.decode('utf-8'), file = f)

def test_bad_status(xibo_session, xibo_api_url_builder):
    """Test raising a Xibo API error for a bad HTTP response status."""
    bad_about_url = xibo_api_url_builder.about_url() + "x"
    xibo_api = XiboApi(xibo_session, xibo_api_url_builder, SAMPLE_XIBO_PAGE_LENGTH)
    with pytest.raises(XiboApiError, match=r'.*HTTP status is \d+, not ok.*'):
        xibo_api.get_response(bad_about_url)

@pytest.mark.skip(reason="Not authorized to use this API service")
def test_about_response(module_file_path, xibo_session, xibo_api_url_builder):
    """Save response from an "about" request to Xibo."""
    xibo_api = XiboApi(xibo_session, xibo_api_url_builder, SAMPLE_XIBO_PAGE_LENGTH)
    xibo_json = xibo_api.get_about()
    save_json(xibo_json, module_file_path)

def test_get_xibo_api_version(mocker):
    """Testing getting the Xibo API version number."""
    xibo_api = XiboApi(None, None, SAMPLE_XIBO_PAGE_LENGTH)
    xibo_api.get_about = mocker.Mock(return_value = SAMPLE_ABOUT_JSON)
    assert xibo_api.get_xibo_api_version() == "1.8.12"

def test_get_datasets_by_code_response(module_file_path, xibo_session, xibo_api_url_builder):
    """Save response from a "dataset" request to Xibo."""
    dataset_code = os.getenv("EVENT_DATASET_CODE")
    if not dataset_code:
        pytest.skip("Define environment variable EVENT_DATASET_CODE")
    xibo_api = XiboApi(xibo_session, xibo_api_url_builder, SAMPLE_XIBO_PAGE_LENGTH)
    xibo_json = xibo_api.get_datasets_by_code(dataset_code)
    save_json(xibo_json, module_file_path)

def test_get_dataset_column_response(module_file_path, xibo_session, xibo_api_url_builder):
    """Save response from a "dataset column" request to Xibo."""
    dataset_id = os.getenv("EVENT_DATASET_ID")
    if not dataset_id:
        pytest.skip("Define environment variable EVENT_DATASET_ID")
    xibo_api = XiboApi(xibo_session, xibo_api_url_builder, REAL_XIBO_PAGE_LENGTH)
    xibo_json = xibo_api.get_dataset_column_by_id(dataset_id)
    save_json(list(xibo_json), module_file_path)

def test_get_response(module_file_path, xibo_session, xibo_api_url_builder):
    """Save response from a "dataset data" request to Xibo."""
    dataset_id = os.getenv("EVENT_DATASET_ID")
    if not dataset_id:
        pytest.skip("Define environment variable EVENT_DATASET_ID")
    xibo_api = XiboApi(xibo_session, xibo_api_url_builder, SAMPLE_XIBO_PAGE_LENGTH)
    url = xibo_api_url_builder.dataset_data_url(dataset_id)
    response = xibo_api.get_response(url, start = 100, length = 7)
    save_response(response, module_file_path)

def test_get_dataset_data(module_file_path, xibo_session, xibo_api_url_builder):
    """Save JSON from a "dataset data" request to Xibo."""
    dataset_id = os.getenv("EVENT_DATASET_ID")
    if not dataset_id:
        pytest.skip("Define environment variable EVENT_DATASET_ID")
    xibo_api = XiboApi(xibo_session, xibo_api_url_builder, REAL_XIBO_PAGE_LENGTH)
    xibo_json = xibo_api.get_dataset_data_by_id(dataset_id)
    save_json(list(xibo_json), module_file_path)

def test_delete_row_response(module_file_path, xibo_session, xibo_api_url_builder):
    """Save response from a "dataset data delete" request to Xibo."""
    row_id = os.getenv("DELETE_ROW_ID")
    if not row_id:
        pytest.skip("Environment variable DELETE_ROW_ID is not defined")
    dataset_id = os.getenv("EVENT_DATASET_ID")
    if not dataset_id:
        pytest.skip("Define environment variable EVENT_DATASET_ID")
    xibo_api = XiboApi(xibo_session, xibo_api_url_builder, SAMPLE_XIBO_PAGE_LENGTH)
    response = xibo_api.delete_dataset_data_by_id(dataset_id, row_id)
    save_response(response, module_file_path)

def test_insert_dataset_data_response(module_file_path, xibo_session, xibo_api_url_builder):
    """Save response from a "dataset data insert" request to Xibo."""
    dataset_id = os.getenv("EVENT_DATASET_ID")
    if not dataset_id:
        pytest.skip("Define environment variable EVENT_DATASET_ID")
    xibo_api = XiboApi(xibo_session, xibo_api_url_builder, SAMPLE_XIBO_PAGE_LENGTH)
    response = xibo_api.insert_dataset_data(dataset_id, SAMPLE_XIBO_EVENT_COLUMNS)
    save_response(response, module_file_path)

def test_update_dataset_data_response(module_file_path, xibo_session, xibo_api_url_builder):
    """Save response from a "dataset data update" request to Xibo."""
    row_id = os.getenv("UPDATE_ROW_ID")
    if not row_id:
        pytest.skip("Environment variable UPDATE_ROW_ID is not defined")
    dataset_id = os.getenv("EVENT_DATASET_ID")
    if not dataset_id:
        pytest.skip("Define environment variable EVENT_DATASET_ID")
    xibo_api = XiboApi(xibo_session, xibo_api_url_builder, SAMPLE_XIBO_PAGE_LENGTH)
    response = xibo_api.update_dataset_data(dataset_id, row_id, SAMPLE_XIBO_EVENT_COLUMNS)
    save_response(response, module_file_path)

def test_get_paged_json_0(mocker):
    """Test getting 0 paged JSON results."""
    xibo_api = XiboApi(None, None, SAMPLE_XIBO_PAGE_LENGTH)
    xibo_api.get_json = mocker.Mock(return_value = SAMPLE_JSON_LIST_0)
    results = xibo_api.get_paged_json(SAMPLE_URL)
    assert list(results) == SAMPLE_JSON_LIST_0
    xibo_api.get_json.assert_called_once_with(SAMPLE_URL, start = 0, length = SAMPLE_XIBO_PAGE_LENGTH)

def test_get_paged_json_1(mocker):
    """Test getting 1 paged JSON result."""
    xibo_api = XiboApi(None, None, SAMPLE_XIBO_PAGE_LENGTH)
    xibo_api.get_json = mocker.Mock(return_value = SAMPLE_JSON_LIST_1)
    results = xibo_api.get_paged_json(SAMPLE_URL)
    assert list(results) == SAMPLE_JSON_LIST_1
    xibo_api.get_json.assert_called_once_with(SAMPLE_URL, start = 0, length = SAMPLE_XIBO_PAGE_LENGTH)

def test_get_paged_json_2(mocker):
    """Test getting 2 paged JSON results."""
    xibo_api = XiboApi(None, None, SAMPLE_XIBO_PAGE_LENGTH)
    xibo_api.get_json = mocker.Mock(return_value = SAMPLE_JSON_LIST_2)
    results = xibo_api.get_paged_json(SAMPLE_URL)
    assert list(results) == SAMPLE_JSON_LIST_2
    xibo_api.get_json.assert_called_once_with(SAMPLE_URL, start = 0, length = SAMPLE_XIBO_PAGE_LENGTH)

def test_get_paged_json_3(mocker):
    """Test getting 3 paged JSON results, requiring two pages."""
    return_values = [SAMPLE_JSON_LIST_3, SAMPLE_JSON_LIST_0]
    expected_calls = [
        mocker.call(SAMPLE_URL, start = 0, length = SAMPLE_XIBO_PAGE_LENGTH),
        mocker.call(SAMPLE_URL, start = SAMPLE_XIBO_PAGE_LENGTH, length = SAMPLE_XIBO_PAGE_LENGTH),
        ]
    xibo_api = XiboApi(None, None, SAMPLE_XIBO_PAGE_LENGTH)
    xibo_api.get_json = mocker.Mock(side_effect = return_values)
    results = xibo_api.get_paged_json(SAMPLE_URL)
    assert list(results) == SAMPLE_JSON_LIST_3
    assert xibo_api.get_json.call_args_list == expected_calls

def test_get_paged_json_4(mocker):
    """Test getting 4 paged JSON results, requiring two pages."""
    return_values = [SAMPLE_JSON_LIST_3, SAMPLE_JSON_LIST_1]
    expected_calls = [
        mocker.call(SAMPLE_URL, start = 0, length = SAMPLE_XIBO_PAGE_LENGTH),
        mocker.call(SAMPLE_URL, start = SAMPLE_XIBO_PAGE_LENGTH, length = SAMPLE_XIBO_PAGE_LENGTH),
        ]
    xibo_api = XiboApi(None, None, SAMPLE_XIBO_PAGE_LENGTH)
    xibo_api.get_json = mocker.Mock(side_effect = return_values)
    results = xibo_api.get_paged_json(SAMPLE_URL)
    assert list(results) == SAMPLE_JSON_LIST_3 + SAMPLE_JSON_LIST_1
    assert xibo_api.get_json.call_args_list == expected_calls

    


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

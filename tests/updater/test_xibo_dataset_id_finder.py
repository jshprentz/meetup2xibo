"""Finding Xibo dataset IDs."""

from meetup2xibo.updater.xibo_api import XiboApi
from meetup2xibo.updater.xibo_dataset_id_finder import XiboDatasetIdFinder
from meetup2xibo.updater.exceptions import DatasetDiscoveryError
import json
import os
import pytest


SAMPLE_JSON_EMPTY_LIST = json.loads("""[]""")

SAMPLE_DATASET_JSON = json.loads("""[
    {
        "code": "novalabsschedule",
        "dataSet": "Nova Labs Schedule",
        "dataSetId": 456,
        "description": "Meetings, classes, and events from Meetup"
    }
]""")

SAMPLE_DATASET_JSON_TOO_MANY = json.loads("""[
    {
        "code": "novalabsschedule",
        "dataSet": "Nova Labs Schedule",
        "dataSetId": 456,
        "description": "Meetings, classes, and events from Meetup"
    },
    {
        "code": "novalabsschedule",
        "dataSet": "Nova Labs Schedule Experimental",
        "dataSetId": 789,
        "description": "Meetings, classes, and events from Meetup"
    }
]""")


def test_discover_dataset_id(mocker):
    """Testing getting the dataset ID."""
    xibo_api = mocker.Mock()
    xibo_api.get_datasets_by_code = mocker.Mock(return_value = SAMPLE_DATASET_JSON)
    finder = XiboDatasetIdFinder(xibo_api)
    assert finder.find_dataset_id("novalabsschedule") == 456
    xibo_api.get_datasets_by_code.assert_called_once_with("novalabsschedule")

def test_discover_dataset_id_none(mocker):
    """Testing getting the dataset ID when there are none."""
    xibo_api = mocker.Mock()
    xibo_api.get_datasets_by_code = mocker.Mock(
            return_value = SAMPLE_JSON_EMPTY_LIST)
    finder = XiboDatasetIdFinder(xibo_api)
    try:
        dataset_id = finder.find_dataset_id("novalabsschedule")
        pytest.fail('Should not find dataset_id {} for code "novalabsschedule"'.format(str(dataset_id)))
    except DatasetDiscoveryError as err:
        assert str(err) == 'No Xibo datasets had code "novalabsschedule"'

def test_discover_dataset_id_too_many(mocker):
    """Testing getting the dataset ID when there are too many."""
    xibo_api = mocker.Mock()
    xibo_api.get_datasets_by_code = mocker.Mock(
            return_value = SAMPLE_DATASET_JSON_TOO_MANY)
    finder = XiboDatasetIdFinder(xibo_api)
    try:
        dataset_id = finder.find_dataset_id("novalabsschedule")
        pytest.fail('Should not find dataset_id {} for code "novalabsschedule"'.format(str(dataset_id)))
    except DatasetDiscoveryError as err:
        assert str(err) == "2 Xibo datasets had code novalabsschedule: Nova Labs Schedule (456),Nova Labs Schedule Experimental (789)"



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

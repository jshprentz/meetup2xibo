"""Tests for Xibo event create, read, update, and delete."""

from meetup2xibo.updater.event_converter import Event
from meetup2xibo.updater.xibo_event import XiboEvent, XiboEventColumnNameManager, XiboEventColumnIdManager
from meetup2xibo.updater.xibo_event_crud import XiboEventCrud
import logging
import pytest


COLUMN_NAMES = XiboEvent(
    xibo_id = "id",
    meetup_id = "Meetup ID",
    name = "Name",
    location = "Location",
    start_time = "ISO Start Time",
    end_time = "ISO End Time"
)

COLUMN_IDS = XiboEvent(
    xibo_id = None,
    meetup_id = '3',
    name = '1',
    location = '2',
    start_time = '4',
    end_time = '5'
)

SAMPLE_JSON_EVENT_1 = {
    "Days Till Start": "-370",
    "ISO End Time": "2018-02-10 17:00:00",
    "ISO Start Time": "2018-02-10 15:00:00",
    "Location": "Orange Bay",
    "Meetup ID": "zvbxrpl",
    "Minutes Past End": "532513",
    "Name": "Nova Labs Open House",
    "Start Time": "3:00 PM",
    "id": "456"
}

SAMPLE_XIBO_EVENT_1 = XiboEvent(
    xibo_id = "456",
    meetup_id = "zvbxrpl",
    name = "Nova Labs Open House",
    location = "Orange Bay",
    start_time = "2018-02-10 15:00:00",
    end_time = "2018-02-10 17:00:00"
)

SAMPLE_XIBO_EVENT_2 = XiboEvent(
    xibo_id = "456",
    meetup_id = "zvbxrpl",
    name = "Nova Labs Special Open House",
    location = "Orange Bay and Atrium",
    start_time = "2018-02-10 15:00:00",
    end_time = "2018-02-10 17:00:00"
)

SAMPLE_MEETUP_EVENT_1 = Event(
    meetup_id = "zvbxrpl",
    name = "Nova Labs Open House",
    location = "Orange Bay",
    places = ["Orange Bay"],
    start_time = "2018-02-10 15:00:00",
    end_time = "2018-02-10 17:00:00"
)

SAMPLE_XIBO_EVENT_1_COLUMNS = {
    '1': "Nova Labs Open House",
    '2': "Orange Bay",
    '3': "zvbxrpl",
    '4': "2018-02-10 15:00:00",
    '5': "2018-02-10 17:00:00"
}

SAMPLE_DATASET_ID = 1122

@pytest.fixture()
def mock_xibo_api(mocker):
    """Return a mock XiboApi."""
    return mocker.MagicMock()

@pytest.fixture()
def crud(mock_xibo_api):
    """Return a XiboEventCrud with a mock Xibo API."""
    column_name_manager = XiboEventColumnNameManager(COLUMN_NAMES)
    column_id_manager = XiboEventColumnIdManager(COLUMN_IDS)
    return XiboEventCrud(mock_xibo_api, SAMPLE_DATASET_ID, column_name_manager, column_id_manager)

def test_get_xibo_events_1(mocker, mock_xibo_api, crud):
    """Test getting one event from Xibo."""
    mock_xibo_api.get_dataset_data_by_id = mocker.Mock(return_value = [SAMPLE_JSON_EVENT_1])
    events = crud.get_xibo_events()
    assert list(events) == [SAMPLE_XIBO_EVENT_1]
    mock_xibo_api.get_dataset_data_by_id.assert_called_once_with(SAMPLE_DATASET_ID)

def test_delete_xibo_event(mocker, mock_xibo_api, crud):
    """Test deleting an event from Xibo."""
    mock_xibo_api.delete_dataset_data_by_id = mocker.Mock()
    events = crud.delete_xibo_event(SAMPLE_XIBO_EVENT_1)
    mock_xibo_api.delete_dataset_data_by_id.assert_called_once_with(SAMPLE_DATASET_ID, "456")

def test_insert_meetup_event(mocker, mock_xibo_api, crud):
    """Test inserting an event from Xibo."""
    mock_xibo_api.insert_dataset_data = mocker.Mock()
    events = crud.insert_meetup_event(SAMPLE_XIBO_EVENT_1)
    mock_xibo_api.insert_dataset_data.assert_called_once_with(
        SAMPLE_DATASET_ID, SAMPLE_XIBO_EVENT_1_COLUMNS)

def test_update_xibo_event(mocker, caplog, mock_xibo_api, crud):
    """Test updating an event from Xibo."""
    caplog.set_level(logging.INFO)
    mock_xibo_api.insert_dataset_data = mocker.Mock()
    events = crud.update_xibo_event(SAMPLE_XIBO_EVENT_2, SAMPLE_MEETUP_EVENT_1)
    mock_xibo_api.update_dataset_data.assert_called_once_with(SAMPLE_DATASET_ID,
        SAMPLE_XIBO_EVENT_2.xibo_id, SAMPLE_XIBO_EVENT_1_COLUMNS)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

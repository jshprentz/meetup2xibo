"""Tests for Xibo event conversions."""

from meetup2xibo.updater.xibo_event import XiboEvent, XiboEventColumnNameManager, XiboEventColumnIdManager
import json

EXAMPLE_COLUMNS_FILE = "tests/updater/example_dataset_columns.json"

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
    meetup_id = 'dataSetColumnId_3',
    name = 'dataSetColumnId_1',
    location = 'dataSetColumnId_2',
    start_time = 'dataSetColumnId_4',
    end_time = 'dataSetColumnId_5'
)

SAMPLE_JSON_EVENT = {
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

SAMPLE_XIBO_EVENT = XiboEvent(
    xibo_id = "456",
    meetup_id = "zvbxrpl",
    name = "Nova Labs Open House",
    location = "Orange Bay",
    start_time = "2018-02-10 15:00:00",
    end_time = "2018-02-10 17:00:00"
)

SAMPLE_XIBO_EVENT_COLUMNS = {
    'dataSetColumnId_1': "Nova Labs Open House",
    'dataSetColumnId_2': "Orange Bay",
    'dataSetColumnId_3': "zvbxrpl",
    'dataSetColumnId_4': "2018-02-10 15:00:00",
    'dataSetColumnId_5': "2018-02-10 17:00:00"
}

def test_json_to_xibo_event():
    """Test converting a retrieved JSON event to an
    internal Xibo event format."""
    manager = XiboEventColumnNameManager(COLUMN_NAMES)
    assert manager.json_to_xibo_event(SAMPLE_JSON_EVENT) == SAMPLE_XIBO_EVENT

def test_json_to_column_ids():
    """Test converting retrieved JSON column metadata
    to a Xibo event loaded with column IDs."""
    json_columns = json.load(open(EXAMPLE_COLUMNS_FILE))
    manager = XiboEventColumnNameManager(COLUMN_NAMES)
    assert manager.json_to_column_ids(json_columns) == COLUMN_IDS

def test_event_to_columns():
    """Test converting a Xibo event to a dictionary indexed
    by column IDs."""
    manager = XiboEventColumnIdManager(COLUMN_IDS)
    assert manager.event_to_columns(SAMPLE_XIBO_EVENT) == SAMPLE_XIBO_EVENT_COLUMNS


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

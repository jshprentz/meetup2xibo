from .context import meetup2xibo
from meetup2xibo.xibo_db import Xibo_DB_Query_Maker


COLUMN_NAMES = {
    "meetup_id": "foo_meetup_id",
    "name": "foo_name",
    "location": "foo_location",
    "start_time": "foo_start_time",
    "end_time": "foo_end_time",
    "xibo_id": "id"
}

EXPECTED_INSERT_QUERY = "INSERT INTO dataset_1 " \
    "(`foo_meetup_id`, `foo_name`, `foo_location`, `foo_start_time`, `foo_end_time`) " \
    "VALUES (%(meetup_id)s, %(name)s, %(location)s, %(start_time)s, %(end_time)s)"

EXPECTED_UPDATE_QUERY = "UPDATE dataset_2 SET " \
    "`foo_meetup_id` = %(meetup_id)s, " \
    "`foo_name` = %(name)s, " \
    "`foo_location` = %(location)s, " \
    "`foo_start_time` = %(start_time)s, " \
    "`foo_end_time` = %(end_time)s " \
    "WHERE id = %(xibo_id)s"

EXPECTED_DELETE_QUERY = "DELETE FROM dataset_3 where id = %s"

EXPECTED_SELECT_QUERY = "SELECT " \
    "`id`, `foo_meetup_id`, `foo_name`, `foo_location`, `foo_start_time`, `foo_end_time` " \
    "FROM dataset_4"


def test_insert_query():
    """Test that the expected insert query is generated."""
    query_maker = Xibo_DB_Query_Maker(COLUMN_NAMES)
    assert EXPECTED_INSERT_QUERY == query_maker.insert_query(1)

def test_update_query():
    """Test that the expected update query is generated."""
    query_maker = Xibo_DB_Query_Maker(COLUMN_NAMES)
    assert EXPECTED_UPDATE_QUERY == query_maker.update_query(2)

def test_delete_query():
    """Test that the expected delete query is generated."""
    query_maker = Xibo_DB_Query_Maker(COLUMN_NAMES)
    assert EXPECTED_DELETE_QUERY == query_maker.delete_query(3)

def test_select_query():
    """Test that the expected select query is generated."""
    query_maker = Xibo_DB_Query_Maker(COLUMN_NAMES)
    assert EXPECTED_SELECT_QUERY == query_maker.select_query(4)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

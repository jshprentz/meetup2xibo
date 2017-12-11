from collections import namedtuple
import logging
import MySQLdb


XiboEvent = namedtuple("XiboEvent", "xibo_id meetup_id name location start_time end_time")

MEETUP_EVENT_COLUMN_NAMES = ["Meetup ID", "Name", "Location", "ISO Start Time", "ISO End Time"]

INSERT_COLUMN_NAMES = ", ".join("`{}`".format(name) for name in MEETUP_EVENT_COLUMN_NAMES)
SELECT_COLUMN_NAMES = "`id`, " + INSERT_COLUMN_NAMES

UPDATE_ASSIGNMENTS = ", ".join("`{}` = %s".format(name) for name in MEETUP_EVENT_COLUMN_NAMES)


class Xibo_DB_Query_Maker:

    """Makes queries for accessing events in the Xibo database."""

    def __init__(self, dataset_number, column_names):
        """Initialize with a dataset number and a dictionary of
        Meetup event column names."""
        self.dataset_number = dataset_number
        self.column_names = column_names

    def insert_query(self):
        """Return a query to insert new events."""
        insert_fields = [field for field in XiboEvent._fields if field != "xibo_id"]
        insert_columns = [self.column_names[field] for field in insert_fields]
        columns = ", ".join("`{}`".format(name) for name in insert_columns)
        values = ", ".join("%({})s".format(field) for field in insert_fields)
        return "INSERT INTO dataset_{} ({}) VALUES ({})".format(self.dataset_number, columns, values)

    def update_query(self):
        """Return a query to update an event."""
        update_fields = [field for field in XiboEvent._fields if field != "xibo_id"]
        update_columns = [self.column_names[field] for field in update_fields]
        assignments = ["`{}` = %({})s".format(column, field) for column, field in zip(update_columns, update_fields)]
        return "UPDATE dataset_{} SET {} WHERE id = %(xibo_id)s".format(self.dataset_number, ", ".join(assignments))

    def delete_query(self):
        """Return a query to delete an event."""
        return "DELETE FROM dataset_{} where id = %s".format(self.dataset_number)

    def select_query(self):
        """Return a query to select events."""
        xibo_column_names = self.column_names.copy()
        xibo_column_names['xibo_id'] = "id"
        select_fields = [field for field in XiboEvent._fields]
        select_columns = [xibo_column_names[field] for field in select_fields]
        columns = ", ".join("`{}`".format(name) for name in select_columns)
        return "SELECT {} FROM dataset_{}".format(columns, self.dataset_number)


class Xibo_DB_Connection:

    """Hides details of accessing a Xibo database."""

    logger = logging.getLogger("Xibo_DB_Connection")

    def __init__(self, db_connection):
        """Initialize with a database connection."""
        self.db_connection = db_connection

    def get_xibo_events(self):
        """Get a list of Xibo events from the database."""
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT {} FROM dataset_2".format(SELECT_COLUMN_NAMES))
        event_tuples = cursor.fetchall()
        cursor.close()
        return (XiboEvent(*event_tuple) for event_tuple in event_tuples)

    def insert_meetup_event(self, meetup_event):
        """Insert a Meetup event into the database."""
        cursor = self.db_connection.cursor()
        sql = "INSERT INTO dataset_2 ({}) VALUES (%s, %s, %s, %s, %s)".format(INSERT_COLUMN_NAMES)
        cursor.execute(sql, meetup_event)
        self.logger.info("Inserted %s", meetup_event)
        cursor.close()

    def update_xibo_event(self, xibo_event, meetup_event):
        """Update a Xibo event in the database with a Meetup event."""
        cursor = self.db_connection.cursor()
        sql = "UPDATE dataset_2 SET {} WHERE id = %s".format(UPDATE_ASSIGNMENTS)
        cursor.execute(sql, meetup_event + (xibo_event.xibo_id,))
        self.logger.info("Updated from %s", xibo_event)
        self.logger.info("Updated to %s", meetup_event)
        cursor.close()

    def delete_xibo_event(self, xibo_event):
        """Delete a Xibo event from the database."""
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM dataset_2 where id = %s", (xibo_event.xibo_id, ))
        self.logger.info("Delected %s", xibo_event)
        cursor.close()


def connect_to_xibo_db(**args):
    """Make a connection to the Xibo database with a dictionary
    of database connection arguments."""
    return Xibo_DB_Connection(MySQLdb.connect(**args))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

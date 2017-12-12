from collections import namedtuple
import logging
import time
import MySQLdb


XiboEvent = namedtuple("XiboEvent", "xibo_id meetup_id name location start_time end_time")


class Xibo_DB_Query_Maker:

    """Makes queries for accessing events in the Xibo database."""

    def __init__(self, column_names, delete_minutes_after_event):
        """Initialize with a a dictionary of Meetup event column names
        and a number of minutes after an event."""
        self.column_names = column_names
        self.delete_minutes_after_event = delete_minutes_after_event

    def insert_query(self, dataset_number):
        """Return a query to insert new events."""
        insert_fields = [field for field in XiboEvent._fields if field != "xibo_id"]
        insert_columns = [self.column_names[field] for field in insert_fields]
        columns = ", ".join("`{}`".format(name) for name in insert_columns)
        values = ", ".join("%({})s".format(field) for field in insert_fields)
        return "INSERT INTO dataset_{} ({}) VALUES ({})".format(dataset_number, columns, values)

    def update_query(self, dataset_number):
        """Return a query to update an event."""
        update_fields = [field for field in XiboEvent._fields if field != "xibo_id"]
        update_columns = [self.column_names[field] for field in update_fields]
        assignments = ["`{}` = %({})s".format(column, field) for column, field in zip(update_columns, update_fields)]
        return "UPDATE dataset_{} SET {} WHERE id = %(xibo_id)s".format(dataset_number, ", ".join(assignments))

    def delete_query(self, dataset_number):
        """Return a query to delete an event."""
        return self.delete_query_now(dataset_number, time.time())

    def delete_query_now(self, dataset_number, now):
        """Return a query to delete a future starting event or an event
        that ended some time past. Now is measured in epoch seconds."""
        future = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now + 120))
        past = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now - self.delete_minutes_after_event * 60))
        return "DELETE FROM dataset_{dataset_number} WHERE id = %s AND " \
            "(`{start_time_column}` > '{future}' OR `{end_time_column}` < '{past}')".format(
            dataset_number = dataset_number,
            end_time_column = self.column_names['end_time'],
            start_time_column = self.column_names['start_time'],
            future = future,
            past = past)

    def select_query(self, dataset_number):
        """Return a query to select events."""
        select_fields = [field for field in XiboEvent._fields]
        select_columns = [self.column_names[field] for field in select_fields]
        columns = ", ".join("`{}`".format(name) for name in select_columns)
        return "SELECT {} FROM dataset_{}".format(columns, dataset_number)


class Xibo_DB_Connection:

    """Hides details of accessing a Xibo database."""

    logger = logging.getLogger("Xibo_DB_Connection")

    def __init__(self, db_connection, query_maker):
        """Initialize with a database connection and a query maker."""
        self.db_connection = db_connection
        self.query_maker = query_maker

    def make_queries(self, dataset_code):
        """Make various SQL queries to access the dataset identified by an API code."""
        dataset_number = self.get_dataset_number(dataset_code)
        self.logger.debug("dataset_number=%s", dataset_number)
        self.insert_query = self.query_maker.insert_query(dataset_number)
        self.update_query = self.query_maker.update_query(dataset_number)
        self.delete_query = self.query_maker.delete_query(dataset_number)
        self.select_query = self.query_maker.select_query(dataset_number)

    def get_dataset_number(self, dataset_code):
        """Get the id number for the dataset holding Meetup events."""
        query = "SELECT DataSetID FROM dataset WHERE code = %s"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (dataset_code, ))
        result = cursor.fetchone()
        if result == None:
            raise KeyError('cannot find dataset "{}"'.format(dataset_code))
        cursor.close()
        return result[0]

    def get_xibo_events(self):
        """Get a list of Xibo events from the database."""
        cursor = self.db_connection.cursor()
        cursor.execute(self.select_query)
        event_tuples = cursor.fetchall()
        cursor.close()
        return (XiboEvent(*event_tuple) for event_tuple in event_tuples)

    def insert_meetup_event(self, meetup_event):
        """Insert a Meetup event into the database."""
        cursor = self.db_connection.cursor()
        cursor.execute(self.insert_query, meetup_event._asdict())
        self.logger.info("Inserted %s", meetup_event)
        cursor.close()

    def update_xibo_event(self, xibo_event, meetup_event):
        """Update a Xibo event in the database with a Meetup event."""
        updates = meetup_event._asdict()
        updates["xibo_id"] = xibo_event.xibo_id
        cursor = self.db_connection.cursor()
        cursor.execute(self.update_query, updates)
        self.logger.info("Updated from %s", xibo_event)
        self.logger.info("Updated to %s", meetup_event)
        cursor.close()

    def delete_xibo_event(self, xibo_event):
        """Delete a Xibo event from the database."""
        cursor = self.db_connection.cursor()
        cursor.execute(self.delete_query, (xibo_event.xibo_id, ))
        self.logger.info("Deleted %s", xibo_event)
        cursor.close()


def connect_to_xibo_db(db_connect_args, column_names, db_config):
    """Make a connection to the Xibo database with a dictionary
    of database connection arguments, a dictionary mapping internal
    names to database column names, and other database configurations."""
    query_maker = Xibo_DB_Query_Maker(column_names, db_config["delete_minutes_after_event"])
    db_connection = MySQLdb.connect(**db_connect_args)
    xibo_connection = Xibo_DB_Connection(db_connection, query_maker)
    xibo_connection.make_queries(db_config["xibo_dataset_code"])
    return xibo_connection

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

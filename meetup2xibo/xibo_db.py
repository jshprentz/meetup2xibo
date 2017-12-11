from collections import namedtuple
import logging
import MySQLdb


XiboEvent = namedtuple("XiboEvent", "xibo_id meetup_id name location start_time end_time")


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
        select_fields = [field for field in XiboEvent._fields]
        select_columns = [self.column_names[field] for field in select_fields]
        columns = ", ".join("`{}`".format(name) for name in select_columns)
        return "SELECT {} FROM dataset_{}".format(columns, self.dataset_number)


class Xibo_DB_Connection:

    """Hides details of accessing a Xibo database."""

    logger = logging.getLogger("Xibo_DB_Connection")

    def __init__(self, db_connection, query_maker):
        """Initialize with a database connection and a query maker."""
        self.db_connection = db_connection
        self.query_maker = query_maker

    def get_xibo_events(self):
        """Get a list of Xibo events from the database."""
        query = self.query_maker.select_query()
        self.logger.debug(query)
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        event_tuples = cursor.fetchall()
        cursor.close()
        return (XiboEvent(*event_tuple) for event_tuple in event_tuples)

    def insert_meetup_event(self, meetup_event):
        """Insert a Meetup event into the database."""
        query = self.query_maker.insert_query()
        self.logger.debug(query)
        cursor = self.db_connection.cursor()
        cursor.execute(query, meetup_event._asdict())
        self.logger.info("Inserted %s", meetup_event)
        cursor.close()

    def update_xibo_event(self, xibo_event, meetup_event):
        """Update a Xibo event in the database with a Meetup event."""
        updates = meetup_event._asdict()
        updates["xibo_id"] = xibo_event.xibo_id
        query = self.query_maker.update_query()
        self.logger.debug(query)
        cursor = self.db_connection.cursor()
        cursor.execute(query, updates)
        self.logger.info("Updated from %s", xibo_event)
        self.logger.info("Updated to %s", meetup_event)
        cursor.close()

    def delete_xibo_event(self, xibo_event):
        """Delete a Xibo event from the database."""
        query = self.query_maker.delete_query()
        self.logger.debug(query)
        cursor = self.db_connection.cursor()
        cursor.execute(query, (xibo_event.xibo_id, ))
        self.logger.info("Deleted %s", xibo_event)
        cursor.close()


def connect_to_xibo_db(db_connect_args, column_names):
    """Make a connection to the Xibo database with a dictionary
    of database connection arguments."""
    query_maker = Xibo_DB_Query_Maker(2, column_names)
    db_connection = MySQLdb.connect(**db_connect_args)
    return Xibo_DB_Connection(db_connection, query_maker)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

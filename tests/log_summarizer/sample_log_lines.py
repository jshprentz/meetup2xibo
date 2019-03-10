"""Provides time ordered sample log lines."""

START_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:53,454 - INFO - meetup2xibo - Start meetup2xibo 2.0.1"

END_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:14,566 - INFO - meetup2xibo - End meetup2xibo 2.0.1"

INSERT_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:12,865 - INFO - XiboEventCrud - " \
    "Inserted Event(meetup_id='tmnbrqyzhbhb', name='Maker Faire Organizing Team', " \
    "location='Classroom A', start_time='2019-05-05 18:00:00', end_time='2019-05-05 20:00:00')"

INSERT_FIELDS = [
    ('meetup_id', 'tmnbrqyzhbhb'),
    ('name', 'Maker Faire Organizing Team'),
    ('location', 'Classroom A'),
    ('start_time', '2019-05-05 18:00:00'),
    ('end_time', '2019-05-05 20:00:00'),
    ]

UPDATE_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:59,273 - INFO - XiboEventCrud - Updated " \
    "from XiboEvent(xibo_id='423', meetup_id='259565142', name='EMPOWER2MAKE', " \
    "location='Nova Labs', start_time='2019-04-14 08:00:00', end_time='2019-04-14 10:00:00')\n" \
    "2019-03-04 06:{minutes:02d}:59,274 - INFO - XiboEventCrud - Updated to " \
    "Event(meetup_id='259565142', name='EMPOWER2MAKE', location='Orange Bay', " \
    "start_time='2019-04-14 08:00:00', end_time='2019-04-14 10:00:00')"

UPDATE_BEFORE_FIELDS = [
    ('xibo_id', '423'),
    ('meetup_id', '259565142'),
    ('name', 'EMPOWER2MAKE'),
    ('location', 'Nova Labs'),
    ('start_time', '2019-04-14 08:00:00'),
    ('end_time', '2019-04-14 10:00:00'),
    ]

UPDATE_AFTER_FIELDS = [
    ('meetup_id', '259565142'),
    ('name', 'EMPOWER2MAKE'),
    ('location', 'Orange Bay'),
    ('start_time', '2019-04-14 08:00:00'),
    ('end_time', '2019-04-14 10:00:00'),
    ]

DELETE_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:57,083 - INFO - XiboEventCrud - Deleted " \
    "XiboEvent(xibo_id='36', meetup_id='258645498', name='DIYbio: Microfluidics', " \
    "location='Classroom A', start_time='2019-03-03 14:00:00', end_time='2019-03-03 16:00:00')"

DELETE_FIELDS = [
    ('xibo_id', '36'),
    ('meetup_id', '258645498'),
    ('name', 'DIYbio: Microfluidics'),
    ('location', 'Classroom A'),
    ('start_time', '2019-03-03 14:00:00'),
    ('end_time', '2019-03-03 16:00:00'),
    ]

UNKNOWN_LOCATION_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:11,441 - WARNING - LocationChooser - " \
    "Unknown location for PartialEvent(meetup_id='259565055', name='EMPOWER2MAKE', " \
    "start_time='2019-04-12 16:00:00', end_time='2019-04-12 18:00:00', venue_name='', find_us='')"


class SampleLogLines:

    """Provides time ordered sample log lines."""

    def __init__(self, start_minutes = 0):
        """Initialize with a starting time in minutes."""
        self.minutes = start_minutes

    def make_line(self, template):
        """Make a line from a template and increment the time."""
        line = template.format(minutes = self.minutes)
        self.minutes += 1
        return line

    def start_line(self):
        """Return a start line."""
        return self.make_line(START_TEMPLATE)

    def end_line(self):
        """Return an end line."""
        return self.make_line(END_TEMPLATE)

    def insert_line(self):
        """Return an insert line."""
        return self.make_line(INSERT_TEMPLATE)

    def update_line(self):
        """Return an update line."""
        return self.make_line(UPDATE_TEMPLATE)

    def delete_line(self):
        """Return a delete line."""
        return self.make_line(DELETE_TEMPLATE)

    def unknown_location_line(self):
        """Return an unknown_ line."""
        return self.make_line(UNKNOWN_LOCATION_TEMPLATE)

    @property
    def insert_fields(self):
        """return fields that should be extracted from an insert log line."""
        return INSERT_FIELDS

    @property
    def delete_fields(self):
        """return fields that should be extracted from an delete log line."""
        return DELETE_FIELDS

    @property
    def update_before_fields(self):
        """return fields that should be extracted from an update from log
        line."""
        return UPDATE_BEFORE_FIELDS

    @property
    def update_after_fields(self):
        """return fields that should be extracted from an update to log
        line."""
        return UPDATE_AFTER_FIELDS


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

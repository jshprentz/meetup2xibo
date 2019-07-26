"""Provides time ordered sample log lines."""

from meetup2xibo.log_summarizer.conflict import Conflict
from meetup2xibo.log_summarizer.event import Event
from meetup2xibo.log_summarizer.log_lines import InsertEventLogLine, \
    UpdateEventLogLine, DeleteEventLogLine, UnknownLocationLogLine, \
    EventLocationLogLine, SpecialLocationLogLine, RetireEventLogLine
from meetup2xibo.log_summarizer.log_parser import SpecialLocation


DATE_TIME_TEMPLATE = "2019-03-04 06:{minutes:02d}:12"

START_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:53,454 - INFO - meetup2xibo - Start meetup2xibo 2.0.1"

END_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:14,566 - INFO - meetup2xibo - End meetup2xibo 2.0.1"

INSERT_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:12,865 - INFO - XiboEventCrud - " \
    "Inserted Event(meetup_id='tmnbrqyzhbhb', name='Maker Faire Organizing Team', " \
    "location='Classroom A', places=['Classroom A'], " \
    "start_time='2019-05-05 18:00:00', end_time='2019-05-05 20:00:00')"

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
    "places=['Orange Bay'], " \
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

RETIRE_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:48,266 - INFO - XiboEventCrud - Retired " \
    "XiboEvent(meetup_id='257907613', name='Barking Mad Planning Meeting', " \
    "location='Conference Room 3', start_time='2019-03-10 14:00:00', " \
    "end_time='2019-03-10 16:00:00', xibo_id='59')"

RETIRE_FIELDS = [
    ('meetup_id', '257907613'),
    ('name', 'Barking Mad Planning Meeting'),
    ('location', 'Conference Room 3'),
    ('start_time', '2019-03-10 14:00:00'),
    ('end_time', '2019-03-10 16:00:00'),
    ('xibo_id', '59'),
    ]

UNKNOWN_LOCATION_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:11,441 - WARNING - LocationChooser - " \
    "Unknown location for PartialEvent(meetup_id='259565055', name='EMPOWER2MAKE', " \
    "start_time='2019-04-12 16:00:00', end_time='2019-04-12 18:00:00', venue_name='', find_us='')"

UNKNOWN_LOCATION_FIELDS = [
    ('meetup_id', '259565055'),
    ('name', 'EMPOWER2MAKE'),
    ('start_time', '2019-04-12 16:00:00'),
    ('end_time', '2019-04-12 18:00:00'),
    ('venue_name', ''),
    ('find_us', ''),
    ]

SPECIAL_LOCATION_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:05,290 - WARNING - SpecialEventsMonitor - " \
    "No longer needed SpecialLocation(meetup_id='258645498', " \
    "location='Orange Bay', override=False, comment='Just testing')"

SPECIAL_LOCATION_FIELDS = [
    ('meetup_id', '258645498'),
    ('location', 'Orange Bay'),
    ('override', False),
    ('comment', 'Just testing'),
    ]

EVENT_LOCATION_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:25,738 - DEBUG - EventConverter - " \
    "Location='Woodshop' MeetupEvent=PartialEvent(meetup_id='259405866', " \
    "name='Customized Wooden Beer Caddy', start_time='2019-03-17 10:00:00', " \
    "end_time='2019-03-17 12:00:00', venue_name='Nova Labs (Woodshop)', " \
    "find_us='[Woodshop Red area]')"

EVENT_LOCATION = 'Woodshop'

EVENT_LOCATION_FIELDS = [
    ('meetup_id', '259405866'),
    ('name', 'Customized Wooden Beer Caddy'),
    ('start_time', '2019-03-17 10:00:00'),
    ('end_time', '2019-03-17 12:00:00'),
    ('venue_name', 'Nova Labs (Woodshop)'),
    ('find_us', '[Woodshop Red area]'),
    ]

START_CONFLICT_ANALYSIS_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:27,521 - INFO - ConflictAnalyzer - " \
    "Start conflict analysis"

CHECKED_PLACE_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:16,418 - INFO - CheckedPlace - " \
    "Name='Conference Room 1'"

SCHEDULE_CONFLICT_TEMPLATE = \
    "2019-03-04 06:{minutes:02d}:54,246 - INFO - CheckedPlace - " \
    "Schedule conflict: place='Conference Room 2' " \
    "Conflict(start_time='2019-09-03 19:00:00', end_time='2019-09-03 " \
    "21:00:00', events=[Event(meetup_id='vzgnvqyzmbfb', name='Computational " \
    "Mathematics: P=NP for students and engineers at Nova Labs', " \
    "location='Conference Room 2', start_time='2019-09-03 19:00:00', " \
    "end_time='2019-09-03 21:00:00', places=['Conference Room 2']), " \
    "Event(meetup_id='whkcdryzmbfb', name='National Drone Science University " \
    "(NDSU) Drone Science', location='Conference Room 2', " \
    "start_time='2019-09-03 19:00:00', end_time='2019-09-03 21:00:00', " \
    "places=['Conference Room 2'])])" 


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

    def date_time(self):
        """Return an ISO formatted date/time."""
        return self.make_line(DATE_TIME_TEMPLATE)

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

    def retire_line(self):
        """Return a retire line."""
        return self.make_line(RETIRE_TEMPLATE)

    def unknown_location_line(self):
        """Return an unknown location line."""
        return self.make_line(UNKNOWN_LOCATION_TEMPLATE)

    def special_location_line(self):
        """Return a special location line."""
        return self.make_line(SPECIAL_LOCATION_TEMPLATE)

    def event_location_line(self):
        """Return an event location line."""
        return self.make_line(EVENT_LOCATION_TEMPLATE)

    def start_conflict_analysis_line(self):
        """Return a start conflict analysis line."""
        return self.make_line(START_CONFLICT_ANALYSIS_TEMPLATE)

    def checked_place_line(self):
        """Return a checked place line."""
        return self.make_line(CHECKED_PLACE_TEMPLATE)

    def schedule_conflict_line(self):
        """Return a conflict line."""
        return self.make_line(SCHEDULE_CONFLICT_TEMPLATE)

    @property
    def insert_fields(self):
        """return fields that should be extracted from an insert log line."""
        return INSERT_FIELDS

    @property
    def delete_fields(self):
        """return fields that should be extracted from a delete log line."""
        return DELETE_FIELDS

    @property
    def retire_fields(self):
        """return fields that should be extracted from a retire log line."""
        return RETIRE_FIELDS

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

    @property
    def unknown_location_fields(self):
        """return fields that should be extracted from an unknown location log
        line."""
        return UNKNOWN_LOCATION_FIELDS

    def make_insert_log_line(self):
        """Return an insert log line object."""
        event = Event.from_fields(INSERT_FIELDS)
        date_time = self.date_time()
        return InsertEventLogLine(date_time, event)

    def make_update_log_line(self):
        """Return an update log line object."""
        before_event = Event.from_fields(UPDATE_BEFORE_FIELDS)
        after_event = Event.from_fields(UPDATE_AFTER_FIELDS)
        date_time = self.date_time()
        return UpdateEventLogLine(date_time, before_event, after_event)

    def make_delete_log_line(self):
        """Return a delete log line object."""
        event = Event.from_fields(DELETE_FIELDS)
        date_time = self.date_time()
        return DeleteEventLogLine(date_time, event)

    def make_retire_log_line(self):
        """Return a retire log line object."""
        event = Event.from_fields(RETIRE_FIELDS)
        date_time = self.date_time()
        return RetireEventLogLine(date_time, event)

    def make_unknown_location_log_line(self, venue_name=''):
        """Return an unknown location log line object with an optional
        venue name."""
        event = Event.from_fields(
                UNKNOWN_LOCATION_FIELDS + [('venue_name', venue_name)])
        date_time = self.date_time()
        return UnknownLocationLogLine(date_time, event)

    def make_special_location_log_line(self):
        """Return a special location log line object."""
        special_location = SpecialLocation(**dict(SPECIAL_LOCATION_FIELDS))
        date_time = self.date_time()
        return SpecialLocationLogLine(date_time, special_location)

    def make_event_location_log_line(self, location=EVENT_LOCATION):
        """Return an event location log line object, possibly overriding the
        location."""
        event = Event.from_fields(EVENT_LOCATION_FIELDS)
        date_time = self.date_time()
        return EventLocationLogLine(date_time, location, event)

    def make_schedule_conflict(self):
        """Return a schedule conflict for the conflict line."""
        return Conflict(
            start_time='2019-09-03 19:00',
            end_time='2019-09-03 21:00',
            events=[
                Event(
                    meetup_id='vzgnvqyzmbfb',
                    name='Computational Mathematics: P=NP for students and engineers at Nova Labs', 
                    location='Conference Room 2',
                    start_time='2019-09-03 19:00', 
                    end_time='2019-09-03 21:00',
                    places=['Conference Room 2']), 
                Event(
                    meetup_id='whkcdryzmbfb',
                    name='National Drone Science University (NDSU) Drone Science',
                    location='Conference Room 2', 
                    start_time='2019-09-03 19:00',
                    end_time='2019-09-03 21:00', 
                    places=['Conference Room 2'])
                ])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

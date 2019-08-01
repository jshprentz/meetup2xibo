"""Retrieve events from Meetup, extract data to display on signs, and update
Xibo."""

from collections import namedtuple


XiboSessionScope = namedtuple(
        "XiboSessionScope",
        "meetup_events cancelled_meetup_events xibo_session")

XiboEventCrudScope = namedtuple(
        "XiboEventCrudScope",
        "event_dataset_id event_column_ids")


class Meetup2Xibo:

    """Downloads Meetup events into a Xibo database."""

    def __init__(
            self, meetup_events_retriever, conflict_analyzer,
            event_converter, site_cert_assurer, oauth2_session_starter,
            enter_xibo_session_scope):
        """Initialize with a Meetup events retriever, an event converter, a
        site certificate assurer, an OAuth2 session starter, and a Xibo sesson
        scope entrance function """
        self.meetup_events_retriever = meetup_events_retriever
        self.conflict_analyzer = conflict_analyzer
        self.event_converter = event_converter
        self.site_cert_assurer = site_cert_assurer
        self.oauth2_session_starter = oauth2_session_starter
        self.enter_xibo_session_scope = enter_xibo_session_scope

    def run(self):
        """Run the Meetup to Xibo conversion."""
        meetup_events = self.retreive_meetup_events()
        cancelled_meetup_events = self.retreive_cancelled_meetup_events()
        self.convert(meetup_events, cancelled_meetup_events)
        self.conflict_analyzer.analyze_conflicts(meetup_events)

    def convert(self, meetup_events, cancelled_meetup_events):
        """Convert Meetup events to Xibo events."""
        xibo_session = self.start_xibo_session()
        self.update_xibo_events(
                meetup_events, cancelled_meetup_events, xibo_session)

    def retreive_meetup_events(self):
        """Retrieve a list of Meetup events."""
        json_events = self.meetup_events_retriever.retrieve_events_json()
        return self.extract_events_from_json(
                json_events,
                self.event_converter.convert)

    def retreive_cancelled_meetup_events(self):
        """Retrieve a list of cancelled Meetup events."""
        retriever = self.meetup_events_retriever
        json_events = retriever.retrieve_cancelled_events_json()
        return self.extract_events_from_json(
                json_events,
                self.event_converter.convert_cancelled)

    def extract_events_from_json(self, json_events, convert):
        """Extract event tuples from a list of Meetup JSON events with a
        conversion function."""
        return [convert(event_json) for event_json in json_events]

    def start_xibo_session(self):
        """Return a new web session with the Xibo API server."""
        self.site_cert_assurer.assure_site_cert()
        return self.oauth2_session_starter.start_session()

    def update_xibo_events(
            self, meetup_events, cancelled_meetup_events, xibo_session):
        """Update events stored in Xibo to match the Meetup events."""
        xibo_session_scope = XiboSessionScope(
            meetup_events, cancelled_meetup_events, xibo_session)
        processor = self.enter_xibo_session_scope(xibo_session_scope)
        processor.run()


class XiboSessionProcessor:

    """Retreives event dataset metadata from Xibo."""

    def __init__(
            self, event_dataset_code, dataset_id_finder, column_name_manager,
            xibo_api, enter_xibo_event_crud_scope):
        """Initialize with an event dataset code, a Xibo dataset ID finder, a
        Xibo event column name manager, a Xibo API manager, and a function to
        enter a Xibo event CRUD scope."""
        self.event_dataset_code = event_dataset_code
        self.dataset_id_finder = dataset_id_finder
        self.column_name_manager = column_name_manager
        self.xibo_api = xibo_api
        self.enter_xibo_event_crud_scope = enter_xibo_event_crud_scope

    def run(self):
        """Retrieve event dataset metadata from Xibo."""
        dataset_id = self.lookup_dataset_id()
        column_ids = self.map_dataset_column_names(dataset_id)
        self.update_xibo_events(dataset_id, column_ids)

    def lookup_dataset_id(self):
        """Lookup the dataset ID for a dataset code."""
        return self.dataset_id_finder.find_dataset_id(self.event_dataset_code)

    def map_dataset_column_names(self, dataset_id):
        """Map the dataset column names to IDs for a given dataset."""
        json_columns = self.xibo_api.get_dataset_column_by_id(dataset_id)
        return self.column_name_manager.json_to_column_ids(json_columns)

    def update_xibo_events(self, event_dataset_id, event_column_ids):
        """Update events stored in Xibo to match the Meetup events."""
        xibo_event_crud_scope = XiboEventCrudScope(
                event_dataset_id, event_column_ids)
        processor = self.enter_xibo_event_crud_scope(xibo_event_crud_scope)
        processor.run()


class XiboEventCrudProcessor:
    """Updates events stored in Xibo to match the Meetup events."""

    def __init__(self, xibo_event_crud, provide_event_updater):
        """Initialize a Xibo event CRUD manager, and a function that provides
        an event updater.  """
        self.xibo_event_crud = xibo_event_crud
        self.provide_event_updater = provide_event_updater

    def run(self):
        """Update events stored in Xibo to match the Meetup events."""
        xibo_events = self.xibo_event_crud.get_xibo_events()
        event_updater = self.provide_event_updater(
            self.xibo_event_crud, xibo_events)
        event_updater.update_xibo()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

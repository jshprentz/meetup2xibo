"""Application scope holds command line arguments and
environment variables needed by the application."""


from .special_location import SpecialLocation
from .scope_cache import ScopeCache
import meetup2xibo
import logging
from collections import namedtuple

APP_NAME = "meetup2xibo"
XIBO_PAGE_LENGTH = 50

SECONDS_PER_HOUR = 60 * 60
SECONDS_PER_DAY = 24 * SECONDS_PER_HOUR

PhraseLocation = namedtuple("PhraseLocation", "phrase place")


class ApplicationScope:

    """Application scope provides configuration values."""

    def __init__(self, args, env_vars):
        """Initialize with parsed command line arguments and a careful
        environment variable dictionary."""
        self._args = args
        self._env_vars = env_vars
        self._event_suppressor_cache = ScopeCache()

    @property
    def app_name(self):
        return APP_NAME

    @property
    def conflict_places(self):
        return self._env_vars.json("CONFLICT_PLACES")

    @property
    def conflicts(self):
        return self._args.conflicts

    @property
    def containing_places(self):
        return self._env_vars.json("CONTAINING_PLACES")

    @property
    def delete_after_end_seconds(self):
        return int(self._env_vars["DELETE_AFTER_END_HOURS"]) \
                * SECONDS_PER_HOUR

    @property
    def delete_before_start_seconds(self):
        return int(self._env_vars["DELETE_BEFORE_START_HOURS"]) \
                * SECONDS_PER_HOUR

    @property
    def delete_until_future_seconds(self):
        return int(self._env_vars["DELETE_UNTIL_FUTURE_DAYS"]) \
                * SECONDS_PER_DAY

    @property
    def debug(self):
        return self._args.debug

    @property
    def default_location(self):
        return self._env_vars["DEFAULT_LOCATION"]

    @property
    def default_places(self):
        return self._env_vars.json("DEFAULT_PLACES")

    @property
    def end_time_column_name(self):
        return self._env_vars["END_TIME_COLUMN_NAME"]

    @property
    def event_dataset_code(self):
        return self._env_vars["EVENT_DATASET_CODE"]

    def event_suppressor(self, event_suppressor_provider):
        return self._event_suppressor_cache.get(event_suppressor_provider)

    @property
    def ignore_cancelled_after_seconds(self):
        return int(self._env_vars["IGNORE_CANCELLED_AFTER_DAYS"]) \
                * SECONDS_PER_DAY

    @property
    def location_column_name(self):
        return self._env_vars["LOCATION_COLUMN_NAME"]

    @property
    def place_phrases(self):
        return self._env_vars.json("PLACE_PHRASES")

    @property
    def place_phrase_tuples(self):
        return (
            PhraseLocation(**dict) for dict in self.place_phrases
        )

    @property
    def logfile(self):
        return self._args.logfile

    @property
    def log_level(self):
        return logging.DEBUG if self.debug else logging.INFO

    @property
    def mappings(self):
        return self._args.mappings

    @property
    def meetup_events_wanted(self):
        return self._env_vars["MEETUP_EVENTS_WANTED"]

    @property
    def meetup_group_url_name(self):
        return self._env_vars["MEETUP_GROUP_URL_NAME"]

    @property
    def meetup_id_column_name(self):
        return self._env_vars["MEETUP_ID_COLUMN_NAME"]

    @property
    def more_place_phrases(self):
        return self._env_vars.json("MORE_PLACE_PHRASES")

    @property
    def more_place_phrase_tuples(self):
        return (
            PhraseLocation(**dict) for dict in self.more_place_phrases
        )

    @property
    def name_column_name(self):
        return self._env_vars["NAME_COLUMN_NAME"]

    @property
    def site_ca_path(self):
        return self._env_vars["SITE_CA_PATH"]

    @property
    def site_url(self):
        return self._env_vars["SITE_URL"]

    @property
    def special_locations(self):
        return self._env_vars.json("SPECIAL_LOCATIONS")

    @property
    def special_locations_dict(self):
        return {
                d["meetup_id"]: SpecialLocation(**d)
                for d in self.special_locations}

    @property
    def start_time_column_name(self):
        return self._env_vars["START_TIME_COLUMN_NAME"]

    @property
    def suppressed_event_ids(self):
        return self._env_vars.json("SUPPRESSED_EVENT_IDS")

    @property
    def timezone(self):
        return self._env_vars["TIMEZONE"]

    @property
    def verbose(self):
        return self._args.verbose

    @property
    def version(self):
        return meetup2xibo.__version__

    @property
    def warnings(self):
        return self._args.warnings

    @property
    def xibo_client_id(self):
        return self._env_vars["XIBO_CLIENT_ID"]

    @property
    def xibo_client_secret(self):
        return self._env_vars["XIBO_CLIENT_SECRET"]

    @property
    def xibo_host(self):
        return self._env_vars["XIBO_HOST"]

    @property
    def xibo_id_column_name(self):
        return self._env_vars["XIBO_ID_COLUMN_NAME"]

    @property
    def xibo_page_length(self):
        return XIBO_PAGE_LENGTH

    @property
    def xibo_port(self):
        return self._env_vars["XIBO_PORT"]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

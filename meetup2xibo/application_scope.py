"""Application scope holds command line arguments and
environment variables needed by the application."""


import logging
import json
from collections import namedtuple


VERSION = "2.0.1"
APP_NAME = "meetup2xibo"
XIBO_PAGE_LENGTH = 50


PhraseLocation = namedtuple("PhraseLocation", "phrase location")


class ApplicationScope:

    """Application scope provides configuration values."""

    def __init__(self, args, env_vars):
        """Initialize with parsed command line arguments and an
        environment variable dictionary."""
        self._args = args
        self._env_vars = env_vars

    @property
    def app_name(self):
        return APP_NAME

    @property
    def debug(self):
        return self._args.debug

    @property
    def default_location(self):
        return self._env_vars["DEFAULT_LOCATION"]

    @property
    def end_time_column_name(self):
        return self._env_vars["END_TIME_COLUMN_NAME"]

    @property
    def event_dataset_code(self):
        return self._env_vars["EVENT_DATASET_CODE"]

    @property
    def location_column_name(self):
        return self._env_vars["LOCATION_COLUMN_NAME"]

    @property
    def location_phrases(self):
        return self._env_vars["LOCATION_PHRASES"]

    @property
    def location_phrase_tuples(self):
        return (
            PhraseLocation(**dict) for dict in
            json.loads(self.location_phrases)
        )

    @property
    def logfile(self):
        return self._args.logfile

    @property
    def log_level(self):
        return logging.DEBUG if self.debug else logging.INFO

    @property
    def meetup_api_key(self):
        return self._env_vars["MEETUP_API_KEY"]

    @property
    def meetup_group_url_name(self):
        return self._env_vars["MEETUP_GROUP_URL_NAME"]

    @property
    def meetup_id_column_name(self):
        return self._env_vars["MEETUP_ID_COLUMN_NAME"]

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
    def start_time_column_name(self):
        return self._env_vars["START_TIME_COLUMN_NAME"]

    @property
    def verbose(self):
        return self._args.verbose

    @property
    def version(self):
        return VERSION

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
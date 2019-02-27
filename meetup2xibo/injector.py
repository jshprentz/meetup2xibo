"""Test generating the Xibo API."""

from .logging_context import LoggingContext
from .meetup2xibo import Meetup2Xibo, XiboSessionProcessor, XiboEventCrudProcessor
from .meetup_api import MeetupEventsRetriever
from .location_extractor import LocationExtractor
from .event_converter import EventConverter
from .event_updater import EventUpdater
from .xibo_api_url_builder import XiboApiUrlBuilder
from .site_cert_assurer import SiteCertAssurer
from .oauth2_session_starter import Oauth2SessionStarter
from .xibo_api import XiboApi
from .xibo_dataset_id_finder import XiboDatasetIdFinder
from .xibo_event import XiboEvent, XiboEventColumnNameManager, XiboEventColumnIdManager
from .xibo_event_crud import XiboEventCrud
from pathlib import Path
import os
import certifi

def inject_meetup_2_xibo(application_scope):
    """Return a Meetup to Xibo converter
    configured by an application scope."""
    return Meetup2Xibo(
        inject_logging_context(application_scope),
        inject_meetup_events_retriever(application_scope),
        inject_event_converter(application_scope),
        inject_site_cert_assurer(application_scope),
        inject_oauth2_session_starter(application_scope),
        inject_enter_xibo_session_scope(application_scope),
        )

def inject_logging_context(application_scope):
    """Return a logging context
    configured by an application scope."""
    return LoggingContext(
        app_name = application_scope.app_name,
        version = application_scope.version,
        log_level = application_scope.log_level,
        filename = application_scope.logfile,
        verbose = application_scope.verbose)

def inject_meetup_events_retriever(application_scope):
    """Return a Meetup events retriever
    configured by an application scope."""
    return MeetupEventsRetriever(
        group_url_name = application_scope.meetup_group_url_name,
        api_key = application_scope.meetup_api_key)

def inject_location_extractor(application_scope):
    """Return a loaction exctractor
    configured by an application scope."""
    return LocationExtractor.from_location_phrases(
        application_scope.location_phrase_tuples,
        application_scope.default_location)

def inject_event_converter(application_scope):
    """Return an event converter
    configured by an application scope."""
    return EventConverter(
        inject_location_extractor(application_scope))

def inject_xibo_api_url_builder(application_scope):
    """Return a Xibo API URL builder
    configured by an application scope."""
    return XiboApiUrlBuilder(
        application_scope.xibo_host,
        application_scope.xibo_port)

def inject_site_cert_assurer(application_scope):
    """Return a site certificate assurer
    configured by an application scope."""
    return SiteCertAssurer(
        sys_ca_path = certifi.where(),
        site_ca_path = application_scope.site_ca_path,
        site_url = inject_cert_validation_url(application_scope),
        user_agent = inject_user_agent(application_scope))

def inject_cert_validation_url(application_scope):
    """Return the URL for certificate validation
    configured by an application scope."""
    return inject_xibo_api_url_builder(application_scope) \
        .cert_validation_url()

def inject_xibo_token_url(application_scope):
    """Return the URL for retrieving tokens
    configured by an application scope."""
    return inject_xibo_api_url_builder(application_scope) \
        .access_token_url()

def inject_user_agent(application_scope):
    """Return the user agent string for web requests
    configured by an application scope."""
    return "{}/{}".format(
        application_scope.app_name,
        application_scope.version)

def inject_oauth2_session_starter(application_scope):
    """Return an Oauth2SessionStarter configured by
    an application scope."""
    return Oauth2SessionStarter(
        application_scope.xibo_client_id,
        application_scope.xibo_client_secret,
        inject_xibo_token_url(application_scope),
        inject_user_agent(application_scope))

def inject_enter_xibo_session_scope(application_scope):
    """Return a function configured by an application scope that provides a
    Xibo session processor configured by an application scope and a Xibo
    session scope."""
    def enter(xibo_session_scope):
        return inject_xibo_session_processor(application_scope, xibo_session_scope)
    return enter

def inject_xibo_session_processor(application_scope, xibo_session_scope):
    """Return a Xibo session processor configured by an application scope and a
    Xibo session scope."""
    return XiboSessionProcessor(
        application_scope.event_dataset_code,
        inject_xibo_dataset_id_finder(application_scope, xibo_session_scope),
        inject_column_name_manager(application_scope),
        inject_xibo_api(application_scope, xibo_session_scope),
        inject_enter_xibo_event_crud_scope(application_scope, xibo_session_scope)
        )

def inject_xibo_api(application_scope, xibo_session_scope):
    """Return a Xibo API manager
    configured by an application scope and a Xibo session scope."""
    return XiboApi(
        xibo_session_scope.xibo_session,
        inject_xibo_api_url_builder(application_scope),
        application_scope.xibo_page_length)

def inject_xibo_dataset_id_finder(application_scope, xibo_session_scope):
    """Return a Xibo dataset ID finder
    configured by an application scope and a Xibo session scope."""
    return XiboDatasetIdFinder(
        inject_xibo_api(application_scope, xibo_session_scope))

def inject_column_name_manager(application_scope):
    """Return a Xibo column name manager
    configured by an application scope."""
    return XiboEventColumnNameManager(
        inject_xibo_column_names(application_scope))

def inject_xibo_column_names(application_scope):
    """Return Xibo event column names
    configured by an application scope."""
    return XiboEvent(
        xibo_id = application_scope.xibo_id_column_name,
        meetup_id = application_scope.meetup_id_column_name,
        name = application_scope.name_column_name,
        location = application_scope.location_column_name,
        start_time = application_scope.start_time_column_name,
        end_time = application_scope.end_time_column_name
        )

def inject_enter_xibo_event_crud_scope(application_scope, xibo_session_scope):
    """Return a function configured by an application scope that provides a
    Xibo event CRUD processor configured by an application scope and a Xibo
    session scope."""
    def enter(xibo_event_crud_scope):
        return inject_xibo_event_crud_processor(application_scope,
            xibo_session_scope, xibo_event_crud_scope)
    return enter

def inject_xibo_event_crud_processor(application_scope,
        xibo_session_scope, xibo_event_crud_scope):
    """Return Xibo event CRUD processor configured by an application scope, a
    Xibo session scope and a Xibo event CRUD scope."""
    return XiboEventCrudProcessor(
        xibo_session_scope.meetup_events,
        inject_xibo_event_crud(application_scope, xibo_session_scope, xibo_event_crud_scope),
        inject_event_updater_provider(xibo_session_scope)
        )

def inject_xibo_event_crud(application_scope, xibo_session_scope, xibo_event_crud_scope):
    """Return a Xibo event CRUD manager
    configured by an application scope, a Xibo session scope and a Xibo event CRUD scope."""
    return XiboEventCrud(
        inject_xibo_api(application_scope, xibo_session_scope),
        xibo_event_crud_scope.event_dataset_id,
        inject_column_name_manager(application_scope),
        inject_xibo_event_column_id_manager(xibo_event_crud_scope)
        )

def inject_xibo_event_column_id_manager(xibo_event_crud_scope):
    """Return a Xibo column ID manager
    configured by a Xibo event CRUD scope."""
    return XiboEventColumnIdManager(xibo_event_crud_scope.event_column_ids)

def inject_event_updater_provider(xibo_session_scope):
    """Return a function that provides an event updater
    configured by a Xibo session scope."""
    def get(xibo_event_crud, xibo_events):
        return EventUpdater(
            xibo_session_scope.meetup_events,
            xibo_events,
            xibo_event_crud
            )
    return get

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Test generating the Xibo API."""

from .logging_application import LoggingApplication
from .logging_context import LoggingContext
from .logging_setup_manager import LoggingSetupManager
from .http_response_error import HttpResponseError
from .exceptions import DatasetDiscoveryError, ContainmentLoopError, \
        JsonConversionError
from .meetup2xibo import Meetup2Xibo, XiboSessionProcessor, \
        XiboEventCrudProcessor
from .meetup_api import MeetupEventsRetriever
from .place_finder import PlaceFinder
from .location_chooser import LocationChooser
from .conflict_analyzer import ConflictAnalyzer, NullConflictAnalyzer
from .conflict_places import ConflictPlaces, ConflictPlacesLoader
from .event_converter import EventConverter
from .event_location import EventLocation
from .event_updater import EventUpdater
from .phrase_mapper import PhraseMapper
from .xibo_api_url_builder import XiboApiUrlBuilder
from .site_cert_assurer import SiteCertAssurer
from .oauth2_session_starter import Oauth2SessionStarter, \
        Oauth2SessionStarterError
from .special_location_monitor import SpecialLocationMonitor
from .time_converter import DateTimeCreator
from .xibo_api import XiboApi
from .xibo_dataset_id_finder import XiboDatasetIdFinder
from .xibo_event import XiboEvent, XiboEventColumnNameManager, \
        XiboEventColumnIdManager
from .xibo_event_crud import XiboEventCrud
from .anti_flapper import AntiFlapper
from ahocorasick import Automaton
from requests_toolbelt import user_agent
from pytz import timezone
import certifi


def inject_logging_application(application_scope):
    """Return a logging application configured by an application scope."""
    return LoggingApplication(
        inject_logging_context(application_scope),
        inject_enter_logging_application_scope(application_scope)
        )


def inject_logging_context(application_scope):
    """Return a logging context configured by an application scope."""
    return LoggingContext(
        app_name=application_scope.app_name,
        description=application_scope.version,
        logging_setup_manager=inject_logging_setup_manager(application_scope),
        no_trace_exceptions=inject_no_trace_exceptions())


def inject_logging_setup_manager(application_scope):
    """Return a logging setup manager configured by an application scope."""
    return LoggingSetupManager(
        log_level=application_scope.log_level,
        filename=application_scope.logfile,
        verbose=application_scope.verbose,
        warnings=application_scope.warnings,
        mappings=application_scope.mappings)


def inject_enter_logging_application_scope(application_scope):
    """Return a function configured by an application scope that provides a
    processor configured by an application scope and a notional logging
    application scope."""
    def enter():
        return inject_meetup2xibo(application_scope)
    return enter


def inject_no_trace_exceptions():
    """Return a tuple listing exception classes that need no traceback."""
    return (
            HttpResponseError,
            ContainmentLoopError,
            DatasetDiscoveryError,
            JsonConversionError,
            Oauth2SessionStarterError)


def inject_meetup_events_retriever(application_scope):
    """Return a Meetup events retriever configured by an application scope."""
    return MeetupEventsRetriever(
        group_url_name=application_scope.meetup_group_url_name,
        events_wanted=application_scope.meetup_events_wanted,
        cancelled_last_time=inject_cancelled_last_time(application_scope))


def inject_location_chooser(application_scope):
    """Return a location builder configured by an application scope."""
    return LocationChooser(
        inject_place_finder(application_scope),
        application_scope.special_locations_dict,
        inject_default_event_location(application_scope))


def inject_place_finder(application_scope):
    """Return a place finder configured by an application scope."""
    return PlaceFinder(inject_phrase_mappers(application_scope))


def inject_phrase_mappers(application_scope):
    """Return a list of phrase mappers configured by an application scope."""
    return [
        inject_places_phrase_mapper(application_scope),
        inject_more_places_phrase_mapper(application_scope),
        ]


def inject_places_phrase_mapper(application_scope):
    """Return a phrase mapper for place phrases configured by an application
    scope."""
    return inject_phrase_mapper(
        application_scope,
        application_scope.place_phrase_tuples)


def inject_more_places_phrase_mapper(application_scope):
    """Return a phrase mapper for more place phrases configured by an
    application scope."""
    return inject_phrase_mapper(
        application_scope,
        application_scope.more_place_phrase_tuples)


def inject_phrase_mapper(application_scope, phrase_tuples):
    """Return a phrase mapper configured by an application scope and a list of
    tuples containing a phrase and its preferred phrase."""
    return PhraseMapper(inject_automaton(), phrase_tuples).setup()


def inject_automaton():
    """Return an Aho-Corasick automaton."""
    return Automaton()


def inject_default_event_location(application_scope):
    """Return an event location for the default location and places configured
    by an application scope."""
    return EventLocation(
        application_scope.default_location,
        application_scope.default_places)


def inject_event_converter(application_scope):
    """Return an event converter configured by an application scope."""
    return EventConverter(
        inject_location_chooser(application_scope),
        inject_date_time_creator(application_scope))


def inject_xibo_api_url_builder(application_scope):
    """Return a Xibo API URL builder configured by an application scope."""
    return XiboApiUrlBuilder(
        application_scope.xibo_host,
        application_scope.xibo_port)


def inject_site_cert_assurer(application_scope):
    """Return a site certificate assurer configured by an application scope."""
    return SiteCertAssurer(
        sys_ca_path=certifi.where(),
        site_ca_path=application_scope.site_ca_path,
        site_url=inject_cert_validation_url(application_scope),
        user_agent=inject_user_agent(application_scope))


def inject_cert_validation_url(application_scope):
    """Return the URL for certificate validation configured by an application
    scope."""
    return inject_xibo_api_url_builder(application_scope) \
        .cert_validation_url()


def inject_xibo_token_url(application_scope):
    """Return the URL for retrieving tokens configured by an application
    scope."""
    return inject_xibo_api_url_builder(application_scope) \
        .access_token_url()


def inject_user_agent(application_scope):
    """Return the user agent string for web requests configured by an
    application scope."""
    return user_agent(
        application_scope.app_name,
        application_scope.version)


def inject_oauth2_session_starter(application_scope):
    """Return an Oauth2SessionStarter configured by an application scope."""
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
        return inject_xibo_session_processor(
                application_scope, xibo_session_scope)
    return enter


def inject_xibo_session_processor(application_scope, xibo_session_scope):
    """Return a Xibo session processor configured by an application scope and a
    Xibo session scope."""
    return XiboSessionProcessor(
        application_scope.event_dataset_code,
        inject_xibo_dataset_id_finder(application_scope, xibo_session_scope),
        inject_column_name_manager(application_scope),
        inject_xibo_api(application_scope, xibo_session_scope),
        inject_enter_xibo_event_crud_scope(
                application_scope, xibo_session_scope)
        )


def inject_xibo_api(application_scope, xibo_session_scope):
    """Return a Xibo API manager configured by an application scope and a Xibo
    session scope."""
    return XiboApi(
        xibo_session_scope.xibo_session,
        inject_xibo_api_url_builder(application_scope),
        application_scope.xibo_page_length)


def inject_xibo_dataset_id_finder(application_scope, xibo_session_scope):
    """Return a Xibo dataset ID finder configured by an application scope and a
    Xibo session scope."""
    return XiboDatasetIdFinder(
        inject_xibo_api(application_scope, xibo_session_scope))


def inject_column_name_manager(application_scope):
    """Return a Xibo column name manager configured by an application scope."""
    return XiboEventColumnNameManager(
        inject_xibo_column_names(application_scope))


def inject_xibo_column_names(application_scope):
    """Return Xibo event column names configured by an application scope."""
    return XiboEvent(
        xibo_id=application_scope.xibo_id_column_name,
        meetup_id=application_scope.meetup_id_column_name,
        name=application_scope.name_column_name,
        location=application_scope.location_column_name,
        start_time=application_scope.start_time_column_name,
        end_time=application_scope.end_time_column_name
        )


def inject_enter_xibo_event_crud_scope(application_scope, xibo_session_scope):
    """Return a function configured by an application scope that provides a
    Xibo event CRUD processor configured by an application scope and a Xibo
    session scope."""
    def enter(xibo_event_crud_scope):
        return inject_xibo_event_crud_processor(
            application_scope, xibo_session_scope, xibo_event_crud_scope)
    return enter


def inject_xibo_event_crud_processor(
        application_scope, xibo_session_scope, xibo_event_crud_scope):
    """Return Xibo event CRUD processor configured by an application scope, a
    Xibo session scope and a Xibo event CRUD scope."""
    return XiboEventCrudProcessor(
        inject_xibo_event_crud(
                application_scope, xibo_session_scope, xibo_event_crud_scope),
        inject_event_updater_provider(application_scope, xibo_session_scope)
        )


def inject_xibo_event_crud(
        application_scope, xibo_session_scope, xibo_event_crud_scope):
    """Return a Xibo event CRUD manager configured by an application scope, a
    Xibo session scope and a Xibo event CRUD scope."""
    return XiboEventCrud(
        inject_xibo_api(application_scope, xibo_session_scope),
        xibo_event_crud_scope.event_dataset_id,
        inject_column_name_manager(application_scope),
        inject_xibo_event_column_id_manager(xibo_event_crud_scope)
        )


def inject_xibo_event_column_id_manager(xibo_event_crud_scope):
    """Return a Xibo column ID manager configured by a Xibo event CRUD
    scope."""
    return XiboEventColumnIdManager(xibo_event_crud_scope.event_column_ids)


def inject_event_updater_provider(application_scope, xibo_session_scope):
    """Return a function that provides an event updater configured by a Xibo
    session scope."""
    def get(xibo_event_crud, xibo_events):
        return EventUpdater(
            xibo_session_scope.meetup_events,
            xibo_session_scope.cancelled_meetup_events,
            xibo_events,
            xibo_event_crud,
            inject_anti_flapper(application_scope),
            inject_special_location_monitor(application_scope)
            )
    return get


def inject_anti_flapper(application_scope):
    """Return an anti-flapper configured by an application scope."""
    return AntiFlapper(
        inject_recent_limit(application_scope),
        inject_current_limit(application_scope),
        inject_future_limit(application_scope)
        )


def inject_special_location_monitor(application_scope):
    """Return a special location monitor configured by an application scope."""
    return SpecialLocationMonitor(application_scope.special_locations_dict)


def inject_tzinfo(application_scope):
    """Return timezone info configured by an application scope."""
    return timezone(application_scope.timezone)


def inject_date_time_creator(application_scope):
    """Return a date/time creator configured by an application scope."""
    return DateTimeCreator(inject_tzinfo(application_scope))


def inject_selected_conflict_analyzer(application_scope):
    """Return the conflict analyzer selected by a command-line argument and
    configured by an application scope."""
    if application_scope.conflicts:
        return inject_conflict_analyzer(application_scope)
    else:
        return inject_null_conflict_analyzer()


def inject_conflict_analyzer(application_scope):
    """Return a conflict analyzer configured by an application scope."""
    return ConflictAnalyzer(inject_conflict_places(application_scope))


def inject_conflict_places(application_scope):
    """Return conflict places configured by an application scope."""
    return ConflictPlacesLoader(
            ConflictPlaces(),
            application_scope.conflict_places,
            application_scope.containing_places
            ).load()


def inject_null_conflict_analyzer():
    """Return a null conflict analyzer."""
    return NullConflictAnalyzer()


def inject_recent_limit(application_scope):
    """Return the recent flapping limit configured by an application scope."""
    return inject_date_time_creator(application_scope).xibo_offset_time(
            -application_scope.delete_after_end_seconds)


def inject_current_limit(application_scope):
    """Return the current flapping limit configured by an application scope."""
    return inject_date_time_creator(application_scope).xibo_offset_time(
            application_scope.delete_before_start_seconds)


def inject_future_limit(application_scope):
    """Return the future flapping limit configured by an application scope."""
    return inject_date_time_creator(application_scope).xibo_offset_time(
            application_scope.delete_until_future_seconds)


def inject_cancelled_last_time(application_scope):
    """Return the last time allowed for cancelled Meetup events configured by
    an application scope."""
    return inject_date_time_creator(application_scope).meetup_offset_time(
            application_scope.ignore_cancelled_after_seconds)


def inject_meetup2xibo(application_scope):
    """Return a Meetup to Xibo converter configured by an application scope."""
    return Meetup2Xibo(
        inject_meetup_events_retriever(application_scope),
        inject_selected_conflict_analyzer(application_scope),
        inject_event_converter(application_scope),
        inject_site_cert_assurer(application_scope),
        inject_oauth2_session_starter(application_scope),
        inject_enter_xibo_session_scope(application_scope),
        )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

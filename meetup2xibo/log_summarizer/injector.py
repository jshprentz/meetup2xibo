"""Injectors."""

from .log_summarizer import LogSummarizer
from .log_parser import make_log_parser_class, Summary
from .location_mapper import LocationMapper
from .start_counter import StartCounter
from .crud_lister import CrudLister
from .conflict_reporter import ConflictReporter
from .renderer import Renderer, EmailRenderer, SummaryRenderer, \
        LocationMappingCsvRenderer, make_jinja2_env


def inject_log_summarizer(application_scope):
    """Return a log summarizer configured by an application scope."""
    return LogSummarizer(
        inject_input_stream(application_scope),
        inject_output_stream(application_scope),
        inject_summary(),
        inject_log_parser(),
        inject_renderer(application_scope)
        )


def inject_summary():
    """Return a summary."""
    return Summary(
        inject_start_counter(),
        inject_crud_lister(),
        inject_conflict_reporter(),
        inject_location_mapper())


def inject_input_stream(application_scope):
    """Return the input stream."""
    return application_scope.infile


def inject_output_stream(application_scope):
    """Return the output stream."""
    return application_scope.outfile


def inject_start_counter():
    """Return an empty program start counter."""
    return StartCounter()


def inject_crud_lister():
    """Return an empty event CRUD lister."""
    return CrudLister()


def inject_conflict_reporter():
    """Return an empty conflict reporter."""
    return ConflictReporter()


def inject_location_mapper():
    """Return a location mapper."""
    return LocationMapper()


def inject_log_parser():
    """Return a function that provides a
    log parser for some text."""
    return make_log_parser_class()


def inject_renderer(application_scope):
    """Inject a renderer."""
    return Renderer(
        application_scope.mappings,
        inject_email_renderer(application_scope),
        inject_summary_renderer(),
        inject_location_mapping_csv_renderer())


def inject_email_renderer(application_scope):
    """Inject an email renderer."""
    return EmailRenderer(
        application_scope.email_to,
        application_scope.email_subject)


def inject_summary_renderer():
    """Inject a log summary renderer."""
    return SummaryRenderer(
        inject_jinja2_env(),
        "summary.html")


def inject_jinja2_env():
    """Returns a Jinja2 environment for templates in this package."""
    return make_jinja2_env(__package__)


def inject_location_mapping_csv_renderer():
    """Return a location mapping CSV renderer."""
    return LocationMappingCsvRenderer()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Injectors."""

from .log_summarizer import LogSummarizer
from .log_parser import make_log_parser_class, Summary
from .start_counter import StartCounter
from .crud_lister import CrudLister
from .renderer import Renderer, make_jinja2_env
from sys import stdin, stdout

def inject_log_summarizer(application_scope):
    """Return a log summarizer configured by an application scope."""
    return LogSummarizer(
        inject_input_stream(application_scope),
        inject_output_stream(application_scope),
        inject_summary(),
        inject_log_parser(),
        inject_renderer()
        )

def inject_summary():
    """Return a summary."""
    return Summary(inject_start_counter(), inject_crud_lister())

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

def inject_log_parser():
    """Return a function that provides a
    log parser for some text."""
    return make_log_parser_class()

def inject_enter_xibo_session_scope(application_scope):
    """Return a function configured by an application scope that provides a
    log parser for some text."""
    def enter(xibo_session_scope):
        return inject_xibo_session_processor(
                application_scope, xibo_session_scope)
    return enter

def inject_renderer():
    """Inject a log summary renderer."""
    return Renderer(
        inject_jinja2_env(),
        "summary.html")

def inject_jinja2_env():
    """Returns a Jinja2 environment for templates in this package."""
    return make_jinja2_env(__package__)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

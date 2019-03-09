"""Injectors."""

from .log_summarizer import LogSummarizer


def inject_log_summarizer(application_scope):
    """Return a log summarizer configured by an application scope."""
    return LogSummarizer()


def inject_enter_xibo_session_scope(application_scope):
    """Return a function configured by an application scope that provides a
    Xibo session processor configured by an application scope and a Xibo
    session scope."""
    def enter(xibo_session_scope):
        return inject_xibo_session_processor(
                application_scope, xibo_session_scope)
    return enter

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

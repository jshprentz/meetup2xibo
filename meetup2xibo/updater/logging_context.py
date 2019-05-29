"""Provide a logging context to open and close loggers and handle otherwise
unhandled exceptions."""

import logging
import logging.handlers


class LoggingContext:

    """Logging context configures logging and reports exit exceptions."""

    def __init__(
            self, app_name, description, logging_setup_manager,
            no_trace_exceptions):
        """Initialize with an application name, a description (such as a
        version number), a logging setup manager, and a tuple of exception
        classes that need no traceback."""
        self.app_name = app_name
        self.description = description
        self.logging_setup_manager = logging_setup_manager
        self.no_trace_exceptions = no_trace_exceptions

    def log_start_end(self, verb):
        """Log the start or end of an application given a verb (Start or
        End)."""
        self._named_logger.info("%s %s %s", verb, self.app_name,
                                self.description)

    def log_exception(self, exc_type, exc_value):
        """Log all but system exit exceptions. Skip traceback for common
        exceptions."""
        if not exc_type or exc_type == SystemExit:
            return
        if isinstance(exc_value, self.no_trace_exceptions):
            self._named_logger.error("%s - %s", exc_type.__name__, exc_value)
        else:
            self._named_logger.exception("Unexpected exception")

    def __enter__(self):
        """Enter a 'with' context and return a named logger."""
        self.logging_setup_manager.setup()
        self._named_logger = logging.getLogger(self.app_name)
        self.log_start_end("Start")
        return self._named_logger

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit a 'with' context, logging any exception and shutting down
        logging."""
        self.log_exception(exc_type, exc_value)
        self.log_start_end("End")
        logging.shutdown()
        return True


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

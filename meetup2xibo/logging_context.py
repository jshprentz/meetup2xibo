"""Provide a logging context to open and close loggers and handloe
otherwise unhandled exceptions."""

import logging
import logging.handlers


FORMATTER = logging.Formatter('{asctime} - {levelname} - {name} - {message}', style='{')


class LoggingContext:

    """Logging context configures logging and reports exit exceptions."""

    def __init__(self, *handlers, log_level = logging.INFO, name=None):
        """Initialize with some handlers, a log level, and a name."""
        self.handlers = handlers
        self.log_level = log_level
        self.name = name

    def setup_root_logger(self):
        """Setup the root logger with the configured handlers and log level."""
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        for handler in self.handlers:
            root_logger.addHandler(handler)

    def __enter__(self):
        """Enter a 'with' context and return a named logger."""
        self.setup_root_logger()
        self.named_logger = logging.getLogger(self.name)
        return self.named_logger

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit a 'with' context, logging any exception and shutting down logging."""
        if exc_type and exc_type != SystemExit:
            self.named_logger.exception("Unexpected exception")
        logging.shutdown()
        return True


def daily_file_handler(filename):
    """Return a file handler that rotates daily at midnight."""
    handler = logging.handlers.TimedRotatingFileHandler(
            filename = filename,
            when = 'midnight',
            backupCount = 5)
    handler.setFormatter(FORMATTER)
    return handler

def stderr_stream_handler():
    """Return a stream handler that logs to standard error."""
    handler = logging.StreamHandler()
    handler.setFormatter(FORMATTER)
    return handler

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

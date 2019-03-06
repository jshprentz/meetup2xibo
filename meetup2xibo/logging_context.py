"""Provide a logging context to open and close loggers and handloe otherwise
unhandled exceptions."""

import logging
import logging.handlers


FORMATTER = logging.Formatter(
        '{asctime} - {levelname} - {name} - {message}',
        style='{')


class LoggingContext:

    """Logging context configures logging and reports exit exceptions."""

    def __init__(
            self, app_name, version, log_level=logging.INFO, filename=None,
            verbose=False, warnings=False, mappings=False):
        """Initialize with an application name and version, a log level,
        an optional log file name, a verbose flag (sending logs to stderr), a
        warnings flag (sending warnings to stderr), and a mappings flag to
        force location mapping logs."""
        self.app_name = app_name
        self.version = version
        self.log_level = log_level
        self.filename = filename
        self.verbose = verbose
        self.warnings = warnings
        self.mappings = mappings

    def setup_root_logger(self):
        """Setup the root logger with the configured handlers and log level."""
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        self.log_to_stderr(root_logger)
        self.log_to_file(root_logger)

    def setup_mappings_logger(self):
        """Setup the mappings logger if requested."""
        if self.mappings:
            logger = logging.getLogger("EventConverter")
            logger.setLevel(logging.DEBUG)

    def log_to_file(self, root_logger):
        """Add a file handler that rotates daily at midnight."""
        if self.filename:
            handler = logging.handlers.TimedRotatingFileHandler(
                    filename=self.filename,
                    when='midnight',
                    backupCount=5)
            handler.setFormatter(FORMATTER)
            root_logger.addHandler(handler)

    def log_to_stderr(self, root_logger):
        """Add a stream handler that logs to standard error."""
        if self.verbose or self.warnings or not self.filename:
            handler = logging.StreamHandler()
            handler.setFormatter(FORMATTER)
            if self.warnings:
                handler.setLevel(logging.WARNING)
            root_logger.addHandler(handler)

    def log_start_end(self, verb):
        """Log the start or end of an application given a verb (Start or
        End)."""
        self._named_logger.info("%s %s %s", verb, self.app_name, self.version)

    def __enter__(self):
        """Enter a 'with' context and return a named logger."""
        self.setup_root_logger()
        self.setup_mappings_logger()
        self._named_logger = logging.getLogger(self.app_name)
        self.log_start_end("Start")
        return self._named_logger

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit a 'with' context, logging any exception and shutting down
        logging."""
        if exc_type and exc_type != SystemExit:
            self._named_logger.exception("Unexpected exception")
        self.log_start_end("End")
        logging.shutdown()
        return True


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

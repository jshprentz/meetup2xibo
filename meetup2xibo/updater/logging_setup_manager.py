"""Sets up the Python logging system."""

import logging
import logging.handlers


FORMATTER = logging.Formatter(
        '{asctime} - {levelname} - {name} - {message}',
        style='{')


class LoggingSetupManager:

    """Logging setup manager configures logging based on flags and other
    options."""

    def __init__(
            self, log_level=logging.INFO, filename=None,
            verbose=False, warnings=False, mappings=False):
        """Initialize with a log level, an optional log file name, a verbose
        flag (sending logs to stderr), a warnings flag (sending warnings to
        stderr), and a mappings flag to force location mapping logs."""
        self.log_level = log_level
        self.filename = filename
        self.verbose = verbose
        self.warnings = warnings
        self.mappings = mappings

    def setup(self):
        """Setup the Python logging system."""
        self.setup_root_logger()
        self.setup_mappings_logger()

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


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

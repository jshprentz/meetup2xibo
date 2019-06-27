"""Loggers of potential event location conflict details."""

import logging


class ConflictLogger:

    """Logs event and place details for later conflict detection."""

    logger = logging.getLogger("ConflictLogger")

    def log(self, partial_event, event_location):
        """Log for later conflict analysis a partial event, its location, and
        its places."""
        self.logger.info(
                "Check conflicts {} Location={!r} Places={}".format(
                        partial_event,
                        event_location.description,
                        event_location.places))


class NullConflictLogger:

    """Logs nothing, but provides the conflict logger interface."""

    def log(self, partial_event, event_location):
        """Log for later conflict analysis a partial event, its location, and
        its places."""
        pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

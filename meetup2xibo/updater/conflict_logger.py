"""Loggers of potential event location conflict details."""

import logging


class ConflictLogger:

    """Logs event and place details for later conflict detection."""

    logger = logging.getLogger("ConflictLogger")

    def __init__(self, conflict_places):
        """Initialize with a list of places to check for conflicts."""
        self.conflict_places = frozenset(conflict_places)

    def log(self, partial_event, event_location):
        """Log for later conflict analysis a partial event, its location, and
        its places."""
        filtered_places = self.filter_conflict_places(event_location.places)
        self.log_possible_conflicts(
                partial_event, event_location, filtered_places)

    def filter_conflict_places(self, places):
        """Given iterable places, return a list of places also in the conflict
        places set."""
        return list(self.conflict_places & set(places))

    def log_possible_conflicts(
            self, partial_event, event_location, filtered_places):
        """Log any possibly conflicting places."""
        if filtered_places:
            self.logger.info(
                    "Check conflicts {} Location={!r} Places={}".format(
                            partial_event,
                            event_location.description,
                            filtered_places))


class NullConflictLogger:

    """Logs nothing, but provides the conflict logger interface."""

    def log(self, partial_event, event_location):
        """Log for later conflict analysis a partial event, its location, and
        its places."""
        pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

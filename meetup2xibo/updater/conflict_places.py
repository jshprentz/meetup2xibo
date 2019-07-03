"""Holds places to check for scheduling conflicts."""

from .places import CheckedPlace, UncheckedPlace
import logging


class ConflictPlaces:

    """Places to check for scheduling conflicts."""

    logger = logging.getLogger("ConflictPlaces")

    def __init__(self):
        """Initialize."""
        self._places = {}

    def named_place(self, place_name):
        """Return the named place if it exists. Return None otherwise."""
        return self._places.get(place_name, None)

    def named_or_unchecked_place(self, place_name):
        """Return the named place if it exists. Return a new unchecked place
        otherwise and add it to conflict places."""
        if place_name not in self._places:
            new_place = UncheckedPlace(place_name)
            self._places[place_name] = new_place
        return self._places[place_name]

    def add_conflict_place(self, place_name):
        """Add a named place to check for conflicts, replacing any previous
        place with the same name."""
        self._places[place_name] = CheckedPlace(place_name)

    def add_containing_place(self, place_name, contained_places):
        """Add a place contiaining other places, given the place name and a
        list of other contained place names."""
        containing_place = self.named_or_unchecked_place(place_name)
        for place in contained_places:
            other_place = self.named_or_unchecked_place(place)
            containing_place.contain(other_place)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

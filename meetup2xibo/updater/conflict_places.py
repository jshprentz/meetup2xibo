"""Holds places to check for scheduling conflicts."""

from .places import CheckedPlace, UncheckedPlace


class ConflictPlaces:

    """Places to check for scheduling conflicts."""

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

    def add_checked_place(self, place_name):
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

    def start_event(self, event):
        """Analyze the start of an event at its places."""
        for place_name in event.places:
            place = self.named_or_unchecked_place(place_name)
            place.start_event_carefully(event)

    def end_event(self, event):
        """Analyze the end of an event at its places."""
        for place_name in event.places:
            place = self.named_or_unchecked_place(place_name)
            place.end_event_carefully(event)

    def log_conflicts(self, end_time):
        """Log conflicts in all places at an end time."""
        for place in self._places.values():
            place.log_conflicts(end_time)

    def log_place_names(self):
        """Log place names."""
        for place in self._places.values():
            place.log_place_name()


class ConflictPlacesLoader:

    """Loads conflict places with checked places and place containment."""

    def __init__(
            self, conflict_places, checked_place_names, containing_places):
        """Initialize with a conflict places holder, a list of checked place
        names, and a list of containing places."""
        self.conflict_places = conflict_places
        self.checked_place_names = checked_place_names
        self.containing_places = containing_places

    def load(self):
        """Load checked and containing places into conflict places. Return the
        conflict places."""
        self.add_checked_places()
        self.add_containing_places()
        return self.conflict_places

    def add_checked_places(self):
        """Add named places to check for conflicts."""
        for place_name in self.checked_place_names:
            self.conflict_places.add_checked_place(place_name)

    def add_containing_places(self):
        """Add places that contain other places."""
        for containing_place in self.containing_places:
            place_name = containing_place["place"]
            contained_places = containing_place["contains"]
            self.conflict_places.add_containing_place(
                    place_name,
                    contained_places)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

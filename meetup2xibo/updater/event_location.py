"""An event's location."""

class EventLocation:

    """An event's location as a textual description and a list of places."""

    def __init__(self, description, places):
        """Initialize with the location description and a list of places."""
        self.description = description
        self.places = places

    def __repr__(self):
        """Return the represention the event location."""
        return '{}({!r}, {!r})'.format(
                self.__class__.__name__,
                self.description,
                self.places)

    def __str__(self):
        """Return the string version of the event location, represented the
        event location solely by its description for compatibility with simple
        location strings."""
        return str(self.description)

    def __hash__(self):
        """Return a hash of the event location elements used in __eq__
        comparisons."""
        return hash(self.description)

    def __eq__(self, other):
        """Return true if this event location is equal the other. Otherwise
        return false."""
        return isinstance(other, EventLocation) \
                and self.description == other.description

    def __bool__(self):
        """Used for truth testing. Return true if the locatiion is non-blank;
        false otherwise."""
        return self.description != ""

    @classmethod
    def from_places(cls, places):
        """Make an event location from a list of places."""
        description = cls.format_place_list(places)
        return cls(description, places)

    @staticmethod
    def format_place_list(places):
        """Format a list of places as an English phrase."""
        if len(places) < 3:
            return " and ".join(places)
        else:
            most_places = ", ".join(places[0:-1])
            return "{}, and {}".format(most_places, places[-1])


NO_LOCATION = EventLocation("", [])


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

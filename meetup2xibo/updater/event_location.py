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


NO_LOCATION = EventLocation("", [])



def format_location_list(locations):
    """Format a list of locations as an English phrase."""
    if len(locations) == 1:
        return locations[0]
    if len(locations) == 2:
        return "{} and {}".format(locations[0], locations[1])
    most_locations = ", ".join(locations[0:-1])
    return "{}, and {}".format(most_locations, locations[-1])


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

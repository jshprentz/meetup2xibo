"""Build locations from partial event components."""

from collections import OrderedDict
import logging


class LocationBuilder:

    """Builds locations from partial event components."""

    logger = logging.getLogger("LocationBuilder")

    def __init__(self, phrase_mappers):
        """Initialize with a list of phrase mappers."""
        self.phrase_mappers = phrase_mappers

    def build_location(self, partial_event):
        """Build a location from a partial Meetup event."""
        locations = self.map_from_phrase_mappers(partial_event)
        if locations:
            deduped_locations = list(OrderedDict.fromkeys(locations))
            return self.format_location_list(deduped_locations)
        else:
            return ""

    def map_from_phrase_mappers(self, partial_event):
        """Try all phrase mappers until on finds phrases in a partial event."""
        locations = []
        for phrase_mapper in self.phrase_mappers:
            locations = self.map_phrases_in_venue(phrase_mapper, partial_event)
            if locations:
                break
        return locations

    @staticmethod
    def map_phrases_in_venue(phrase_mapper, partial_event):
        """Map location phrases in the venue and find us fields of a partial
        event."""
        return phrase_mapper.map_phrases(partial_event.venue_name) \
            + phrase_mapper.map_phrases(partial_event.find_us)

    @staticmethod
    def format_location_list(locations):
        """Format a list of locations as an English phrase."""
        if len(locations) == 1:
            return locations[0]
        if len(locations) == 2:
            return "{} and {}".format(locations[0], locations[1])
        most_locations = ", ".join(locations[0:-1])
        return "{}, and {}".format(most_locations, locations[-1])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

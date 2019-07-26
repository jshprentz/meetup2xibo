"""Builds a place list from partial event components."""

from collections import OrderedDict


class PlaceFinder:

    """Builds a place list from partial event components."""

    def __init__(self, phrase_mappers):
        """Initialize with a list of phrase mappers."""
        self.phrase_mappers = phrase_mappers

    def find_places(self, partial_event):
        """Find a list of places from a partial Meetup event."""
        places = self.map_from_phrase_mappers(partial_event)
        deduped_places = list(OrderedDict.fromkeys(places))
        return deduped_places

    def map_from_phrase_mappers(self, partial_event):
        """Try all phrase mappers until one finds phrases in a partial
        event."""
        places = []
        for phrase_mapper in self.phrase_mappers:
            places = self.map_phrases_in_venue(phrase_mapper, partial_event)
            if places:
                break
        return places

    @staticmethod
    def map_phrases_in_venue(phrase_mapper, partial_event):
        """Map place phrases in the venue and find us fields of a partial
        event."""
        return phrase_mapper.map_phrases(partial_event.venue_name) \
            + phrase_mapper.map_phrases(partial_event.find_us)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

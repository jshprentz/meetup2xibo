"""Extracts locations from Meetup event fields."""

import re
import logging


class LocationExtractor:

    """Extracts locations from Meetup event fields."""

    logger = logging.getLogger("LocationExtractor")

    def __init__(self, location_patterns, default_location):
        """Initialize with a list of tuples containing
        conmpiled location patterns and corresponding locations."""
        self.location_patterns = location_patterns
        self.default_location = default_location

    def extract(self, venue_name, find_us):
        """Extract locations from the Meetup venue name and "how to
        find us" information."""
        venue_name_locations = self.extract_from_text(venue_name)
        find_us_locations = self.extract_from_text(find_us)
        combined_locations = venue_name_locations.union(find_us_locations)
        if not combined_locations:
            self.logger.warning(
                'Cannot extract location. venue_name="{}" find_us="{}"'
                .format(venue_name, find_us))
        return self.format_locations(combined_locations)

    def extract_from_text(self, text):
        """Return a set of locations extracted from text."""
        locations = set()
        for matcher, location in self.location_patterns:
            match = matcher.match(text)
            if match:
                text = "|".join(match.groups())
                locations.add(location)
        return locations

    def format_locations(self, location_set):
        """Format a set of locations as an English phrase."""
        if location_set:
            return self.format_location_list(list(location_set))
        else:
            return self.default_location

    @staticmethod
    def format_location_list(locations):
        """Format a list of locations as an English phrase."""
        if len(locations) == 1:
            return locations[0]
        locations.sort()
        if len(locations) == 2:
            return "{} and {}".format(locations[0], locations[1])
        most_locations = ", ".join(locations[0:-1])
        return "{}, and {}".format(most_locations, locations[-1])

    @classmethod
    def from_location_phrases(cls, location_phrases, default_location):
        """Create an instance from a list of tuples containing
        location phrases and corresponding locations and from a
        default location."""
        location_patterns = []
        for phrase, location in location_phrases:
            words = phrase.split()
            regex = r"(.*)\b{}\b(.*)".format(r"\s+".join(words))
            matcher = re.compile(regex, re.IGNORECASE | re.DOTALL)
            location_patterns.append((matcher, location))
        return cls(location_patterns, default_location)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

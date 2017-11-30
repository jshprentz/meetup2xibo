"""Extracts locations from Meetup event fields."""

import re


NOVA_LABS_LOCATION_PHRASES = [
    ("Classroom A and B", "Classroom A/B"),
    ("Classroom A/B", "Classroom A/B"),
    ("Classroom A", "Classroom A"),
    ("Classroom B", "Classroom B"),
    ("Computer Lab", "Computer Lab"),
    ("Conference room 1", "Conference Room 1"),
    ("Conference room 2", "Conference Room 2"),
    ("Conference room 3", "Conference Room 3"),
    ("Conference rm 1", "Conference Room 1"),
    ("Conference rm 2", "Conference Room 2"),
    ("Conference rm 3", "Conference Room 3"),
    ("Orange Bay", "Orange Bay"),
    ("Orange room", "Orange Bay"),
    ("Blacksmithing", "Blacksmithing Alley outside behind Nova Labs"),
    ("out back", "Blacksmithing Alley outside behind Nova Labs"),
    ("outback", "Blacksmithing Alley outside behind Nova Labs"),
    ("Metalshop", "Metal Shop"),
    ("Metal shop", "Metal Shop"),
    ("Woodshop", "Woodshop"),
    ("Wood shop", "Woodshop"),
]


class LocationExtractor:

    """Extracts locations from Meetup event fields."""

    def __init__(self, location_patterns):
        """Initialize with a list of tuples containing
        conmpiled location patterns and corresponding locations."""
        self.location_patterns = location_patterns

    def extract(self, venue_name, find_us):
        """Extract locations from the Meetup venue name and "how to
        find us" information."""
        venue_name_locations = self.extract_from_text(venue_name)
        find_us_locations = self.extract_from_text(find_us)
        return self.format_locations(venue_name_locations.union(find_us_locations))

    def extract_from_text(self, text):
        """Return a set of locations extracted from text."""
        locations = set()
        for matcher, location in self.location_patterns:
            match = matcher.match(text)
            if match:
                text = "|".join(match.groups())
                locations.add(location)
        return locations

    @staticmethod
    def format_locations(location_set):
        """Format a set of locations as an English phrase."""
        if location_set:
            return LocationExtractor.format_location_list(list(location_set))
        else:
            return "TBD"

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
    def from_location_phrases(cls, location_phrases):
        """Create an instance from a list of tuples containing
        location phrases and corresponding locations."""
        location_patterns = []
        for phrase, location in location_phrases:
            words = phrase.split()
            regex = r"(.*)\b{}\b(.*)".format(r"\s+".join(words))
            matcher = re.compile(regex, re.IGNORECASE | re.DOTALL)
            location_patterns.append((matcher, location))
        return cls(location_patterns)

    @classmethod
    def from_nova_labs(cls):
        """Create an instance from the predefined list of tuples
        containing Nova Labs location phrases and corresponding locations."""
        return cls.from_location_phrases(NOVA_LABS_LOCATION_PHRASES)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

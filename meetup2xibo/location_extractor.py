"""Extracts locations from Meetup event fields."""

import re
import logging


class LocationExtractor:

    """Extracts locations from Meetup event fields."""

    logger = logging.getLogger("LocationExtractor")
    find_us_pattern = re.compile(r'^\s*\[(.*)\]\s*$')

    def __init__(self, location_patterns, default_location, default_location_matcher):
        """Initialize with a list of tuples containing
        conmpiled location patterns and corresponding locations
        and a default location with its pattern matcher."""
        self.location_patterns = location_patterns
        self.default_location = default_location
        self.default_location_matcher = default_location_matcher

    def extract(self, venue_name, find_us):
        """Extract locations from the Meetup venue name and "how to
        find us" information."""
        location_list = self.extract_location_list(venue_name, find_us)
        if location_list:
            return self.format_location_list(location_list)
        else:
            return self.extract_default_location(venue_name, find_us)

    def extract_default_location(self, venue_name, find_us):
        """Extract the default location from the  Meetup venue name
        and "how to find us" information."""
        matcher = self.default_location_matcher
        match = matcher.match(venue_name) or matcher.match(find_us)
        if match:
            self.logger.info(
                'Using default location. venue_name="{}" find_us="{}"'
                .format(venue_name, find_us))
            return self.default_location
        else:
            return self.extract_unknown_location(venue_name, find_us)

    def extract_unknown_location(self, venue_name, find_us):
        """Extract an unknown location  from the  Meetup venue name
        and "how to find us" information."""
        self.logger.warning(
            'Cannot extract location. venue_name="{}" find_us="{}"'
            .format(venue_name, find_us))
        match = self.find_us_pattern.search(find_us)
        if match:
            find_us_content = match.group(1)
        else:
            find_us_content = find_us
        nonempty_phrases = list(filter(None, (phrase.strip() for phrase in [venue_name, find_us_content])))
        if nonempty_phrases:
            return " - ".join(nonempty_phrases)
        else:
            return self.default_location


    def extract_location_list(self, venue_name, find_us):
        """Extract a list of locations from the Meetup venue name
        and "how to find us" information."""
        venue_name_locations = self.extract_from_text(venue_name)
        find_us_locations = self.extract_from_text(find_us)
        return list(venue_name_locations.union(find_us_locations))

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
    def format_location_list(locations):
        """Format a list of locations as an English phrase."""
        if len(locations) == 1:
            return locations[0]
        locations.sort()
        if len(locations) == 2:
            return "{} and {}".format(locations[0], locations[1])
        most_locations = ", ".join(locations[0:-1])
        return "{}, and {}".format(most_locations, locations[-1])

    @staticmethod
    def matcher_from_phrase(phrase):
        """Return a regex matcher for the phase, ignoring case
        and exact spacing."""
        words = phrase.split()
        regex = r"(.*)\b{}\b(.*)".format(r"\s+".join(words))
        return re.compile(regex, re.IGNORECASE | re.DOTALL)

    @classmethod
    def from_location_phrases(cls, location_phrases, default_location):
        """Create an instance from a list of tuples containing
        location phrases and corresponding locations and from a
        default location."""
        location_patterns = []
        for phrase, location in location_phrases:
            matcher = cls.matcher_from_phrase(phrase)
            location_patterns.append((matcher, location))
        default_location_matcher = cls.matcher_from_phrase(default_location)
        return cls(location_patterns, default_location, default_location_matcher)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

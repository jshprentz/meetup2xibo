"""Map phrases to preferred phrases."""

import re
import logging
from collections import namedtuple


PhraseMapping = namedtuple("PhraseMapping", "preferred_phrase phrase_length")
SortableMatch = namedtuple("SortableMatch", "start descending_phrase_length end preferred_phrase")

class PhraseMapper:

    """Rewrites a string, mapping phrases to preferred phrases."""

    logger = logging.getLogger("PhraseMapper")

    def __init__(self, automaton, phrase_tuples):
        """Initialize with an Aho-Corasick automaton and a list of tuples
        containing a phrase and its preferred phrase."""
        self.automaton = automaton
        self.phrase_tuples = phrase_tuples

    def map_phrases(self, text):
        """Return a list of phrases preferred to those found in the text."""
        normalized_text = normalize_text(text)
        matches = self.automaton.iter(normalized_text)
        sortable_matches = [match_to_sortable_match(match)
            for match in matches]
        sortable_matches.sort()
        longest_matches = longest_non_overlapping_matches(sortable_matches)
        return [match.preferred_phrase for match in longest_matches]

    def setup(self):
        """Setup and return the phrase mapper."""
        for phrase, preferred_phrase in self.phrase_tuples:
            normalized_phrase = normalize_text(phrase)
            phrase_mapping = PhraseMapping(preferred_phrase, len(normalized_phrase))
            self.automaton.add_word(normalized_phrase, phrase_mapping)
        self.automaton.make_automaton()
        return self

def normalize_text(text):
    """Normalize a text by converting it to lower case and removing
    excess white space."""
    return " ".join(text.lower().split())

def match_to_sortable_match(match):
    """Return a sortable match given a match tuple.  Matches will be sorted by
    start position and decending by phrase length."""
    end, phrase_mapping = match
    return SortableMatch(
        start = end - phrase_mapping.phrase_length,
        end = end,
        descending_phrase_length = -phrase_mapping.phrase_length,
        preferred_phrase = phrase_mapping.preferred_phrase)

def longest_non_overlapping_matches(sorted_matches):
    """Return a generator of the longest non-overlapping matches from a sorted
    list of matches."""
    start = -1
    for match in sorted_matches:
        if match.start < start:
            continue
        yield match
        start = match.end






# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

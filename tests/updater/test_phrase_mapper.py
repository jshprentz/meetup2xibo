"""Test the phrase mapper used to extract locations."""

import meetup2xibo.updater.phrase_mapper as phrase_mapper
import ahocorasick
from hypothesis import given, assume, example
import hypothesis.strategies as st
import pytest


PHRASES = [
    ("Conf Room A", "Room A"),
    ("Conf Room B", "Room B"),
    ("Rm A", "Room A"),
    ("Rm B", "Room B"),
    ("Rm A and B", "Room A and B"),
    ("Bk Rm", "Back Room"),
    ]

EXPECTED_MAPPINGS = [
    ("", []),
    ("rm a", ["Room A"]),
    ("Rm  B", ["Room B"]),
    ("Bk  rm first", ["Back Room"]),
    ("Rm A and B", ["Room A and B"]),
    ("Rm A and rm a", ["Room A", "Room A"]),
    ("Rm A and bk rm", ["Room A", "Back Room"]),
    ("Bk rm and Rm A", ["Back Room", "Room A"]),
    ]

EXPECTED_NORMALIZED_TEXT = [
    ("", ""),
    ("    ", ""),
    ("ABC", "abc"),
    ("def", "def"),
    ("Ghi Jkl", "ghi jkl"),
    ("  Mno     PQR", "mno pqr"),
    ]

SAMPLE_TEXT = "ab cd, efg 32"
#              0123456789012

EXPECTED_VALID_MATCH_ENDS = [1, 4, 12]

EXPECTED_INVALID_MATCH_ENDS = [0, 2, 3, 5, 7, 8, 9]

phrase_tuples = st.sampled_from(PHRASES)
phrase_tuple_lists = st.lists(phrase_tuples, min_size = 1, max_size = len(PHRASES), unique = True)

@pytest.fixture()
def sample_phrase_mapper():
    """Return a phrase mapper initialized with the test phrases."""
    return phrase_mapper.PhraseMapper(ahocorasick.Automaton(), PHRASES)

@pytest.fixture()
def setup_phrase_mapper(sample_phrase_mapper):
    """Return a setup phrase mapper initialized with the test phrases."""
    return sample_phrase_mapper.setup()

@pytest.mark.parametrize("text, expected_phrases", EXPECTED_MAPPINGS)
def test_map_phrases(text, expected_phrases, setup_phrase_mapper):
    """Test that text maps to a list of expected phrases."""
    phrases = setup_phrase_mapper.map_phrases(text)
    assert phrases == expected_phrases

@given(phrase_tuples = phrase_tuple_lists)
def test_map_phrases_ordered(phrase_tuples, setup_phrase_mapper):
    """Test that phrases are mapped in order."""
    patterns, expected_phrases = zip(*phrase_tuples)
    text = ", ".join(patterns)
    phrases = setup_phrase_mapper.map_phrases(text)
    assert phrases == list(expected_phrases)
    
def test_setup_returns_phrase_mapper(sample_phrase_mapper):
    """Test that setup returns the phrase mapper."""
    assert sample_phrase_mapper.setup() == sample_phrase_mapper

@pytest.mark.parametrize("text, expected_normalized_text", EXPECTED_NORMALIZED_TEXT)
def test_normalize_text(text, expected_normalized_text):
    """Test that normalization removes spaces and converts to lower carse."""
    assert phrase_mapper.normalize_text(text) == expected_normalized_text

def test_match_to_sortable_match():
    """Test converting a match into a sortable match."""
    phrase_mapping = phrase_mapper.PhraseMapping("foo", 3)
    match = (15, phrase_mapping)
    expected_sortable_match = (12, -3, 15, "foo")
    assert phrase_mapper.match_to_sortable_match(match) == expected_sortable_match

@pytest.mark.parametrize("match_end", EXPECTED_VALID_MATCH_ENDS)
def test_is_valid_match_yes(match_end):
    """Test that a match is valid at a given end position in sample text."""
    phrase_mapping = phrase_mapper.PhraseMapping("xx", 2)
    match = (match_end, phrase_mapping)
    assert phrase_mapper.is_valid_match(match, SAMPLE_TEXT)

@pytest.mark.parametrize("match_end", EXPECTED_INVALID_MATCH_ENDS)
def test_is_valid_match_no(match_end):
    """Test that a match is invalid at a given end position in sample text."""
    phrase_mapping = phrase_mapper.PhraseMapping("xx", 2)
    match = (match_end, phrase_mapping)
    assert not phrase_mapper.is_valid_match(match, SAMPLE_TEXT)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

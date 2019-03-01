"""Test the phrase mapper used to extract locations."""

from .context import meetup2xibo
from meetup2xibo.phrase_mapper import PhraseMapper
import meetup2xibo.phrase_mapper as phrase_mapper
import ahocorasick
import pytest


PHRASES = [
    ("Rm A", "Room A"),
    ("Rm B", "Room B"),
    ("Rm A and B", "Room A and B"),
    ("Bk Rm", "Back Room"),
    ]

EXPECTED_MAPPINGS = [
    ("", []),
    ("rm a", ["Room A"]),
    ("Rm  B", ["Room B"]),
    ("Rm A and B", ["Room A and B"]),
    ("Rm A and rm a", ["Room A", "Room A"]),
    ("Rm A and bk rm", ["Room A and B"]),
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


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

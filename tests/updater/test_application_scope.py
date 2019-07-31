"""Tests for application scopes."""

from meetup2xibo.updater.application_scope import ApplicationScope
from meetup2xibo.updater.exceptions import JsonConversionError
import pytest

CONFLICT_PLACES='''[
	"CAD Lab",
	"Classroom A"]'''

CONTAINING_PLACES='''[
    {"place": "Classroom A/B", "contains": ["Classroom A", "Classroom B"]},
    {"place": "Woodshop", "contains": ["Green Way"]}
]'''

DEFAULT_PLACES='[]'

PLACE_PHRASES='''[
    {"phrase": "CAD Lab",		"place": "CAD Lab"},
    {"phrase": "Classroom A",		"place": "Classroom A"}
    ]'''


def test_conflict_places_valid():
    """Test converting a valid conflict places list."""
    scope = ApplicationScope(None, {'CONFLICT_PLACES': CONFLICT_PLACES})
    expected_conflict_places = ["CAD Lab", "Classroom A"]
    assert expected_conflict_places == scope.conflict_places

def test_conflict_places_invalid():
    """Test converting an invalid conflict places list."""
    scope = ApplicationScope(None, {'CONFLICT_PLACES': CONFLICT_PLACES[1:]})
    with pytest.raises(JsonConversionError, match="CONFLICT_PLACES"):
        scope.conflict_places

def test_containing_places_valid():
    """Test converting a valid containing places list."""
    scope = ApplicationScope(None, {'CONTAINING_PLACES': CONTAINING_PLACES})
    expected_containing_place = {
            "place": "Classroom A/B",
            "contains": ["Classroom A", "Classroom B"]}
    assert expected_containing_place == scope.containing_places[0]

def test_containing_places_invalid():
    """Test converting an invalid containing places list."""
    scope = ApplicationScope(None, {'CONTAINING_PLACES': CONTAINING_PLACES[1:]})
    with pytest.raises(JsonConversionError, match="Classroom A/B"):
        scope.containing_places

def test_default_places_valid():
    """Test converting a valid default places list."""
    scope = ApplicationScope(None, {'DEFAULT_PLACES': DEFAULT_PLACES})
    expected_default_places = []
    assert expected_default_places == scope.default_places

def test_default_places_invalid():
    """Test converting an invalid default places list."""
    scope = ApplicationScope(None, {'DEFAULT_PLACES': DEFAULT_PLACES[1:]})
    with pytest.raises(JsonConversionError, match="line 1:"):
        scope.default_places

def test_more_place_phrases_valid():
    """Test converting a valid place phrases list."""
    scope = ApplicationScope(None, {'PLACE_PHRASES': PLACE_PHRASES})
    expected_more_place_phrase = {
            "phrase": "CAD Lab",
            "place": "CAD Lab"}
    assert expected_more_place_phrase == scope.more_place_phrases[0]

def test_more_place_phrases_invalid():
    """Test converting an invalid place phrases list."""
    scope = ApplicationScope(None, {'PLACE_PHRASES': PLACE_PHRASES[1:]})
    expected_pointer_line = r'                                                           \^'
    with pytest.raises(JsonConversionError, match=expected_pointer_line):
        scope.more_place_phrases

def test_more_place_phrases_valid():
    """Test converting a valid more place phrases list."""
    scope = ApplicationScope(None, {'MORE_PLACE_PHRASES': PLACE_PHRASES})
    expected_more_place_phrase = {
            "phrase": "Classroom A",
            "place": "Classroom A"}
    assert expected_more_place_phrase == scope.more_place_phrases[1]

def test_more_place_phrases_invalid():
    """Test converting an invalid more place phrases list."""
    scope = ApplicationScope(None, {'MORE_PLACE_PHRASES': PLACE_PHRASES[1:]})
    with pytest.raises(JsonConversionError, match="line 2:"):
        scope.more_place_phrases


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

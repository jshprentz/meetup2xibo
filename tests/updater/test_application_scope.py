"""Tests for application scopes."""

from meetup2xibo.updater.application_scope import ApplicationScope
from meetup2xibo.updater.exceptions import JsonConversionError
import pytest

CONFLICT_PLACES='''[
	"CAD Lab",
	"Classroom A"]'''

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


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

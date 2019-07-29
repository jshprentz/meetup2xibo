"""Tests for application scopes."""

from meetup2xibo.updater.application_scope import ApplicationScope

VALID_CONFLICT_PLACES='''[
	"CAD Lab",
	"Classroom A"]'''

INVALID_CONFLICT_PLACES='''[
	"CAD Lab"
	"Classroom A"]'''

def test_conflict_places_list_valid():
    """Test converting a valid conflict places list."""
    scope = ApplicationScope(None, {'CONFLICT_PLACES': VALID_CONFLICT_PLACES})
    expected_conflict_places_list = ["CAD Lab", "Classroom A"]
    assert expected_conflict_places_list == scope.conflict_places_list

def test_conflict_places_list_invalid():
    """Test converting an invalid conflict places list."""
    scope = ApplicationScope(None, {'CONFLICT_PLACES': INVALID_CONFLICT_PLACES})
    scope.conflict_places_list

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Test the conflict logger."""

from meetup2xibo.updater.conflict_logger import ConflictLogger
import pytest

SAMPLE_CONFLICT_PLACES = [
    "Classroom A",
    "Classroom A/B",
    "Classroom B",
    "Woodshop"
    ]

@pytest.fixture
def conflict_logger():
    """Return a conflict logger recognizing sample places."""
    return ConflictLogger(SAMPLE_CONFLICT_PLACES)

def test_filter_conflict_places_known(conflict_logger):
    """Test filtering only known places."""
    filtered_places = conflict_logger.filter_conflict_places(SAMPLE_CONFLICT_PLACES)
    assert sorted(filtered_places) == SAMPLE_CONFLICT_PLACES

def test_filter_conflict_places_unknown(conflict_logger):
    """Test filtering only unknown places."""
    unknown_places = ["Nova Labs", "George Washington University"]
    filtered_places = conflict_logger.filter_conflict_places(unknown_places)
    assert filtered_places == []

def test_filter_conflict_places_mixed(conflict_logger):
    """Test filtering known and unknown places."""
    mixed_places = ["Nova Labs", "Woodshop", "George Washington University"]
    filtered_places = conflict_logger.filter_conflict_places(mixed_places)
    assert filtered_places == ["Woodshop"]

def test_filter_conflict_places_none(conflict_logger):
    """Test filtering no places."""
    no_places = []
    filtered_places = conflict_logger.filter_conflict_places(no_places)
    assert filtered_places == []

    

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

"""Test event locations."""


from meetup2xibo.updater.event_location import EventLocation
import pytest


def test_repr():
    """Test that repr returns repr(description string)."""
    location = EventLocation(description="test")
    assert repr(location) == repr("test")

def test_str():
    """Test that str returns str(description string)."""
    location = EventLocation(description="test")
    assert str(location) == str("test")

def test_hash_same():
    """Test that two identical locations have the same hash."""
    location1 = EventLocation(description="test")
    location2 = EventLocation(description="test")
    assert hash(location1) == hash(location2)

def test_hash_different():
    """Test that two different locations have different hashes."""
    location1 = EventLocation(description="test1")
    location2 = EventLocation(description="test2")
    assert hash(location1) != hash(location2)

def test_equals_same():
    """Test that two identical locations are equals."""
    location1 = EventLocation(description="test")
    location2 = EventLocation(description="test")
    assert location1 == location2

def test_equals_different():
    """Test that two different locations are not equals."""
    location1 = EventLocation(description="test1")
    location2 = EventLocation(description="test2")
    assert location1 != location2

def test_bool_true():
    """Test that bool returns true for a non-empty string."""
    location = EventLocation(description="test")
    assert location

def test_bool_false():
    """Test that bool returns false for an empty string."""
    location = EventLocation(description="")
    assert not location

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

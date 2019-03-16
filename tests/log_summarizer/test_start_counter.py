"""Test counting program starts."""

from meetup2xibo.log_summarizer.start_counter import StartCounter
import pytest

@pytest.fixture
def start_counter():
    """Return a start counter."""
    return StartCounter()

def test_count_program_once(start_counter):
    """Test counting one program start."""
    start_counter.count("Foo 1.0.0")
    assert start_counter.counts() == [("Foo 1.0.0", 1)]

def test_count_program_twice(start_counter):
    """Test counting two program starts."""
    start_counter.count("Foo 1.0.0")
    start_counter.count("Foo 1.0.0")
    assert start_counter.counts() == [("Foo 1.0.0", 2)]

def test_count_two_programs(start_counter):
    """Test counting starts of two programs."""
    start_counter.count("Foo 1.0.0")
    start_counter.count("Bar 2.0.0")
    start_counter.count("Foo 1.0.0")
    assert start_counter.counts() == [("Bar 2.0.0", 1), ("Foo 1.0.0", 2)]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent


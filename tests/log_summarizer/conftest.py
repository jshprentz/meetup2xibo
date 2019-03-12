"""Pytest fixtures shared among tests."""

from .sample_log_lines import SampleLogLines
import pytest

@pytest.fixture
def sample_log_lines():
    """Return a sample log line generator."""
    return SampleLogLines()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

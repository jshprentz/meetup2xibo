"""Test the conflict reporter."""

from meetup2xibo.log_summarizer.conflict_reporter import ConflictReporter
import pytest


@pytest.fixture
def conflict_reporter():
    """Return a conflict reporter."""
    return ConflictReporter


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

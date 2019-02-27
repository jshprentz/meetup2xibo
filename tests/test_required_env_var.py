"""Test getting required environment variable values."""

from .context import meetup2xibo
from meetup2xibo.required_env_var import RequiredEnvVar
from meetup2xibo.exceptions import RequiredEnvVarError
import pytest


def test_get_exists(monkeypatch):
    """Test getting an existing environment variable value."""
    monkeypatch.setenv("FOO", "bar")
    requiredEnvVar = RequiredEnvVar ("FOO", "something about foo")
    assert requiredEnvVar.get() == "bar"

def test_get_missing(monkeypatch):
    """Test getting a missing environment variable value."""
    monkeypatch.delenv("FOO", raising = False)
    try:
        requiredEnvVar = RequiredEnvVar ("BLAT", "something about blat")
        value = requiredEnvVar.get()
        pytest.fail("Environment should not contain BLAT with value %s" % repr(value))
    except RequiredEnvVarError as err:
        assert str(err) == "Environment does not contain BLAT: something about blat"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

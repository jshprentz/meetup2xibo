"""Test the careful environment wrapper."""

from meetup2xibo.updater.careful_environment import CarefulEnvironment
from meetup2xibo.updater.exceptions import JsonConversionError, MissingEnvVarError
import pytest


VALID_JSON = '''[
	"CAD Lab",
	"Classroom A"]'''

INVALID_JSON = '''[
	"CAD Lab"
	"Classroom A"]'''

SAMPLE_ENV = {
    "VALID_JSON": VALID_JSON,
    "INVALID_JSON": INVALID_JSON,
    "SAMPLE": "sample"
    }

@pytest.fixture
def careful_env():
    """Return a careful environment with some contents."""
    return CarefulEnvironment(SAMPLE_ENV)

def test_getitem_present(careful_env):
    """Test getting a value from the environment."""
    assert careful_env["SAMPLE"] == "sample"

def test_getitem_missing(careful_env):
    """Test getting a missing environment variable."""
    with pytest.raises(MissingEnvVarError, match="EXAMPLE"):
        careful_env["EXAMPLE"]

def test_json_valid(careful_env):
    """Test loading valid JSON."""
    expected_value = ["CAD Lab", "Classroom A"]
    assert expected_value == careful_env.json("VALID_JSON")

def test_json_invalid(careful_env):
    """Test loading invalid JSON."""
    with pytest.raises(JsonConversionError, match="INVALID_JSON"):
        careful_env.json("INVALID_JSON")

def test_json_missing(careful_env):
    """Test loading missing JSON."""
    with pytest.raises(MissingEnvVarError, match="MISSING_JSON"):
        careful_env.json("MISSING_JSON")

def test_len(careful_env):
    """Test getting the length of the environment."""
    assert len(careful_env) == 3

def test_iter(careful_env):
    """Test getting an iterator over the environment keys."""
    sorted_keys = sorted(iter(careful_env))
    assert sorted_keys == ["INVALID_JSON", "SAMPLE", "VALID_JSON"]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

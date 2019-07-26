"""Test generating the Xibo API."""

from meetup2xibo.updater.xibo_api_url_builder import XiboApiUrlBuilder
from meetup2xibo.updater.site_cert_assurer import assure_site_cert
from meetup2xibo.updater.oauth2_session_starter import Oauth2SessionStarter
from meetup2xibo.updater.place_finder import PlaceFinder
from meetup2xibo.updater.phrase_mapper import PhraseMapper
from .sample_events import SampleEvents
from ahocorasick import Automaton
from pathlib import Path
import os
import pytest

LOCATION_PHRASES = [
    ("Classroom A and B", "Classroom A/B"),
    ("Classroom A/B", "Classroom A/B"),
    ("Classroom A", "Classroom A"),
    ("Conference Rm 2", "Conference Room 2"),
    ("Metal shop", "Metal Shop"),
    ("Metalshop", "Metal Shop"),
    ("Out Back", "Blacksmithing Alley"),
]

DEFAULT_PHRASES = [
    ("Nova Labs", "Nova Labs"),
    ("TBD", "TBD")
]

@pytest.fixture(scope="module")
def location_phrase_mapper():
    """Return a phrase mapper initialized with the location phrases."""
    return PhraseMapper(Automaton(), LOCATION_PHRASES).setup()

@pytest.fixture(scope="module")
def default_phrase_mapper():
    """Return a phrase mapper initialized with the default phrases."""
    return PhraseMapper(Automaton(), DEFAULT_PHRASES).setup()

@pytest.fixture(scope="module")
def phrase_mappers(location_phrase_mapper, default_phrase_mapper):
    """Return a list of phrase mappers."""
    return [location_phrase_mapper, default_phrase_mapper]

@pytest.fixture
def place_finder(phrase_mappers):
    """Return a place finder with the test phrase mappers."""
    return PlaceFinder(phrase_mappers)

@pytest.fixture(scope="module")
def xibo_api_url_builder():
    """Return a Xibo API URL builder for the host and port specified by
    environment variable XIBO_HOST and XIBO_PORT. If XIBO_HOST is
    undefined, return None."""
    host = os.getenv("XIBO_HOST")
    if not host:
        return None
    port = os.getenv("XIBO_PORT")
    return XiboApiUrlBuilder(host, port)

def assure_self_signed_cert(xibo_url):
    """Assure that Python Requests recognizes a self signed certificate."""
    site_ca_path = os.environ.get("SITE_CA")
    if site_ca_path and xibo_url:
        assure_site_cert(site_ca_path, xibo_url)

@pytest.fixture(scope="module")
def optional_xibo_session(xibo_api_url_builder):
    """Return an authorized Xibo API web session configured with
    environment variables. If any variables are undefined, return None."""
    if xibo_api_url_builder is None:
        return None
    xibo_token_url = xibo_api_url_builder.access_token_url()
    xibo_client_id = os.getenv("XIBO_CLIENT_ID")
    xibo_client_secret = os.getenv("XIBO_CLIENT_SECRET")
    if None in [xibo_token_url, xibo_client_id, xibo_client_secret]:
        return None
    assure_self_signed_cert(xibo_api_url_builder.cert_validation_url())
    starter = Oauth2SessionStarter(xibo_client_id, xibo_client_secret, xibo_token_url, "test_xibo_api")
    return starter.start_session()

@pytest.fixture()
def xibo_session(optional_xibo_session):
    """Return an authorized Xibo API web session configured with
    environment variables. If any variables are undefined, skip
    the test."""
    if not optional_xibo_session:
        pytest.skip("Xibo environment variables XIBO_TOKEN_URL, "
                "XIBO_CLIENT_ID, and XIBO_CLIENT_SECRET must be defined.")
    return optional_xibo_session

@pytest.fixture(scope="module")
def module_dir_path(request):
    """Assure a directory exists in this module.
    The directory name is given by the environment variable
    combining the module name and "_DIR".  For example,
    module test_foo.py will use the environment variable
    named TEST_FOO_DIR.  Return the path to the directory
    or None if the environment variable is not set."""
    module_file_path = Path(request.module.__file__)
    env_var_name = "{}_{}".format(module_file_path.stem, "DIR").upper()
    module_dir_name = os.environ.get(env_var_name)
    if not module_dir_name:
        return None
    test_dir = module_file_path.parent
    module_dir = test_dir / module_dir_name
    module_dir.mkdir(mode = 0o775, exist_ok = True)
    return module_dir

@pytest.fixture()
def module_file_path(request, module_dir_path):
    """Return a path in the module's directory to a file
    named for the test function.  Skip the test if there
    is no module directory."""
    if module_dir_path is None:
        pytest.skip("No module directory for this test")
    test_name = request.function.__name__
    return module_dir_path / test_name

@pytest.fixture
def sample_events():
    """Return a sample log line generator."""
    return SampleEvents()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

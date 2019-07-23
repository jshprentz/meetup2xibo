"""Test starting an OAuth2 web session."""

from meetup2xibo.updater.oauth2_session_starter import Oauth2SessionStarter, Oauth2SessionStarterError
from meetup2xibo.updater.site_cert_assurer import assure_site_cert
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MissingTokenError
import os
import pytest


def assure_self_signed_cert():
    """Assure that Python Requests recognizes a self signed certificate."""
    site_ca_path = os.environ.get("SITE_CA")
    xibo_url = os.environ.get("XIBO_URL")
    if site_ca_path and xibo_url:
        assure_site_cert(site_ca_path, xibo_url)

def test_create_session():
    """Test that an OAuth2 session is created."""
    starter = Oauth2SessionStarter("a_client_id", "a_client_secret", "a_token_url", "a_user_agent")
    session = starter.create_session()
    assert isinstance(session, OAuth2Session)

def test_set_user_agent():
    """Test that the user agent header is set."""
    starter = Oauth2SessionStarter("a_client_id", "a_client_secret", "a_token_url", "a_user_agent")
    session = starter.create_session()
    starter.set_user_agent(session)
    assert session.headers["user-agent"] == "a_user_agent"

def test_set_user_agent_none():
    """Test that the user agent header is set to something
    even if the OAuth2 session starter user agent is None."""
    starter = Oauth2SessionStarter("a_client_id", "a_client_secret", "a_token_url", None)
    session = starter.create_session()
    starter.set_user_agent(session)
    assert session.headers["user-agent"] is not None

def test_authorize_session(mocker):
    """Test that a token is fetched to authorize a session."""
    mock_session = mocker.Mock()
    starter = Oauth2SessionStarter("a_client_id", "a_client_secret", "a_token_url", "a_user_agent")
    starter.authorize_session(mock_session)
    mock_session.assert_not_called()
    mock_session.fetch_token.assert_called_once_with(
            token_url = "a_token_url",
            client_id = "a_client_id",
            client_secret = "a_client_secret")

def test_authorize_session_no_token_error(mocker):
    """Test handling a missing token error when trying to authorize a session.."""
    mock_session = mocker.Mock()
    mock_session.fetch_token = mocker.Mock(side_effect=MissingTokenError("Missing access token parameter"))
    starter = Oauth2SessionStarter("a_client_id", "a_client_secret", "a_token_url", "a_user_agent")
    expected_message = r"Cannot start OAuth2 session. " \
            r"URL=a_token_url " \
            r"problem=\(missing_token\) Missing access token parameter"
    with pytest.raises(Oauth2SessionStarterError, match=expected_message):
        starter.authorize_session(mock_session)

@pytest.mark.skipif(not os.getenv("XIBO_TOKEN_URL"),
            reason = "environment variable XIBO_TOKEN_URL needed to test live session")
@pytest.mark.skipif(not os.getenv("XIBO_CLIENT_ID"),
            reason = "environment variable XIBO_CLIENT_ID needed to test live session")
@pytest.mark.skipif(not os.getenv("XIBO_CLIENT_SECRET"),
            reason = "environment variable XIBO_CLIENT_SECRET needed to test live session")
def test_start_session():
    """Test that a session starts with a real token provider."""
    assure_self_signed_cert()
    xibo_token_url = os.getenv("XIBO_TOKEN_URL")
    xibo_client_id = os.getenv("XIBO_CLIENT_ID")
    xibo_client_secret = os.getenv("XIBO_CLIENT_SECRET")
    starter = Oauth2SessionStarter(xibo_client_id, xibo_client_secret, xibo_token_url, "test_start_session")
    session = starter.start_session()
    assert isinstance(session, OAuth2Session)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

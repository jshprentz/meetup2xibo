"""Starts an OAuth2 session."""

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


class Oauth2SessionStarter(object):

    """Creates and authorizes an OAuth2 web session."""

    def __init__(self, client_id, client_secret, token_url, user_agent):
        """Initialize with a client ID and secret, the URL for
        obtaining a token, and an optional user agent."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.user_agent = user_agent

    def start_session(self):
        """Start an authorized OAuth2 web session."""
        session = self.create_session()
        self.set_user_agent(session)
        self.authorize_session(session)
        return session

    def create_session(self):
        """Create an OAuth2 session."""
        client = BackendApplicationClient(client_id=self.client_id)
        return OAuth2Session(client=client)

    def authorize_session(self, session):
        """Authorize an OAuth2 session."""
        session.fetch_token(
                token_url=self.token_url,
                client_id=self.client_id,
                client_secret=self.client_secret)

    def set_user_agent(self, session):
        """Set the user agent for a web session."""
        if self.user_agent:
            session.headers.update({'User-Agent': self.user_agent})

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

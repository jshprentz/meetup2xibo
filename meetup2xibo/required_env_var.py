"""Required environment variables can get their value from the
environment or raise an error."""

import os
from .exceptions import RequiredEnvVarError


class RequiredEnvVar:

    """Required environment variables can get their value from the
    environment or raise an error."""

    def __init__(self, name, description):
        """Initialize with an environment variable name and a description."""
        self.name = name
        self.description = description

    def get(self):
        """Get the value from the environment."""
        value = os.getenv(self.name)
        if value == None:
            raise RequiredEnvVarError(self.missing_message())
        return value

    def missing_message(self):
        """Return a message explaining the missing environment variable."""
        return "Environment does not contain {}: {}".format(self.name, self.description)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

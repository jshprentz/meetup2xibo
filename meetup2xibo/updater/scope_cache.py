"""Scope cache based on Do-It-Yourself Dependency Injection by Chad Parry."""


class ScopeCache:

    """Caches the result from a provider."""

    def __init__(self):
        """Initialize the cache to empty."""
        self._cache = None
        self._empty = True

    def get(self, fresh_provider):
        """Invokes fresh_provider function once, caches the result, and returns
        that same value every time. Not thread safe."""
        if self._empty:
            self._cache = fresh_provider()
            self._empty = False
        return self._cache


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

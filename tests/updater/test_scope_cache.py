"""Tests the scope cache."""

from meetup2xibo.updater.scope_cache import ScopeCache
import pytest

def test_get_one_provider_get(mocker):
    """Test that the provider is invoked only once."""
    provider1 = mocker.Mock(return_value = "abcd")
    provider2 = mocker.Mock(return_value = "wxyz")
    cache = ScopeCache()
    assert cache.get(provider1) == "abcd"
    assert cache.get(provider2) == "abcd"
    provider1.assert_called_once_with()
    provider2.assert_not_called()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent

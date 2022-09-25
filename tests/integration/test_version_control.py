"""Tests the cppython built-in VCS plugin
"""

from pytest_cppython.plugin import VersionControlIntegrationTests

from cppython.plugins.git import Git


class TestGitInterface(VersionControlIntegrationTests[Git]):
    """Integration tests for the Git VCS plugin"""

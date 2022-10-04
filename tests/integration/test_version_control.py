"""Tests the cppython built-in VCS plugin
"""

from pytest_cppython.plugin import VersionControlIntegrationTests

from cppython.plugins.git import Git, GitData


class TestGitInterface(VersionControlIntegrationTests[Git, GitData]):
    """Integration tests for the Git VCS plugin"""

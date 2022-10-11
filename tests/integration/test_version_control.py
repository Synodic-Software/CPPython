"""Tests the cppython built-in VCS plugin
"""

import pytest
from pytest_cppython.plugin import VersionControlIntegrationTests

from cppython.plugins.git import Git


class TestGitInterface(VersionControlIntegrationTests[Git]):
    """Integration tests for the Git VCS plugin"""

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[Git]:
        """A required testing hook that allows type generation

        Returns:
            The VCS type
        """
        return Git

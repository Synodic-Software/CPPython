"""Tests the cppython built-in SCM plugin
"""

import pytest
from pytest_cppython.tests import SCMIntegrationTests

from cppython.plugins.git import GitSCM


class TestGitInterface(SCMIntegrationTests[GitSCM]):
    """Integration tests for the Git SCM plugin"""

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[GitSCM]:
        """A required testing hook that allows type generation

        Returns:
            The SCM type
        """
        return GitSCM

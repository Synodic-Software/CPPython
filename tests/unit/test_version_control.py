"""Unit tests for the cppython VCS plugin
"""

import pytest
from pytest_cppython.plugin import VersionControlUnitTests

from cppython.plugins.git import Git


class TestGitInterface(VersionControlUnitTests[Git]):
    """Unit tests for the Git VCS plugin"""

    @pytest.fixture(name="version_control_type")
    def fixture_version_control_type(self) -> type[Git]:
        """A required testing hook that allows type generation

        Returns:
            The VCS type
        """
        return Git

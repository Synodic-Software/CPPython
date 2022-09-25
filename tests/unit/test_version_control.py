"""TODO
"""

import pytest
from pytest_cppython.plugin import VersionControlUnitTests

from cppython.plugins.git import Git


class TestGitInterface(VersionControlUnitTests[Git]):
    """_summary_"""

    @pytest.fixture(name="version_control_type")
    def fixture_version_control_type(self) -> type[Git]:
        """A required testing hook that allows type generation

        Returns:
            _description_
        """
        return Git

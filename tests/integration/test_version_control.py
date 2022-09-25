"""Tests the cppython built-in VCS plugin
"""

from pytest_cppython.plugin import VersionControlIntegrationTests

from cppython.plugins.git import Git


class TestGitInterface(VersionControlIntegrationTests[Git]):
    """_summary_

    Args:
        CPPythonProjectFixtures: _description_
        InterfaceUnitTests: _description_
    """

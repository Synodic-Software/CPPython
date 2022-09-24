"""TODO
"""

from pytest_cppython.plugin import VersionControlUnitTests

from cppython.plugins.git import Git


class TestGitInterface(VersionControlUnitTests[Git]):
    """_summary_

    Args:
        CPPythonProjectFixtures: _description_
        InterfaceUnitTests: _description_
    """

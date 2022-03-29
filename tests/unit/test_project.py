"""
Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from pytest_mock import MockerFixture

from cppython.data import default_pyproject
from cppython.project import Project, ProjectConfiguration


class TestProject:
    """
    TODO
    """

    def test_construction(self, mocker: MockerFixture):
        """
        Makes sure the project can be created from the default PyProject data
        """

        interface_mock = mocker.MagicMock()
        configuration = ProjectConfiguration()
        Project(configuration, interface_mock, default_pyproject.dict())

    def

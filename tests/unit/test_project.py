"""
Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from cppython_core.schema import Generator
from pytest_mock import MockerFixture

from cppython.data import default_pyproject
from cppython.project import Project, ProjectConfiguration, gather_plugins


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

    def test_plugin_gather(self, mocker: MockerFixture):
        """
        TODO
        """
        mocker.patch("cppython.console._create_pyproject", return_value=default_pyproject)
        plugins = gather_plugins(Generator)

        assert len(plugins) == 0

    def test_generator_data_construction(self):
        """
        TODO
        """

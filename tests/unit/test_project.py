"""
Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from cppython_core.schema import Generator
from pytest_mock import MockerFixture

from cppython.data import default_pyproject
from cppython.project import Project, ProjectBuilder, ProjectConfiguration


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


class TestBuilder:
    """
    TODO
    """

    def test_plugin_gather(self):
        """
        TODO
        """

        configuration = ProjectConfiguration()
        builder = ProjectBuilder(configuration)
        plugins = builder.gather_plugins(Generator)

        assert len(plugins) == 0

    def test_generator_data_construction(self):
        """
        TODO
        """

        configuration = ProjectConfiguration()
        builder = ProjectBuilder(configuration)
        Model = builder.generate_model([])

        # TODO: Add Dummy test

    def test_generator_creation(self):
        """
        TODO
        """

        configuration = ProjectConfiguration()
        builder = ProjectBuilder(configuration)
        generators = builder.create_generators([], default_pyproject)

        # TODO: Add Dummy test

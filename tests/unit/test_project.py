"""
Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from cppython_core.schema import Generator, GeneratorData, PyProject
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

    def test_generator_data_construction(self, mocker: MockerFixture):
        """
        TODO
        """

        configuration = ProjectConfiguration()
        builder = ProjectBuilder(configuration)
        model_type = builder.generate_model([])

        assert model_type.__base__ == PyProject

        generator = mocker.Mock(spec=Generator)
        generator_data = mocker.Mock(spec=GeneratorData)

        generator.name.return_value = "mock"
        generator.data_type.return_value = type(generator_data)
        model_type = builder.generate_model([generator])

        assert model_type.__base__ == PyProject

    def test_generator_creation(self, mocker: MockerFixture):
        """
        TODO
        """

        configuration = ProjectConfiguration()
        builder = ProjectBuilder(configuration)
        generators = builder.create_generators([], default_pyproject)

        assert not generators

        generator = mocker.Mock(spec=Generator)
        generators = builder.create_generators([generator], default_pyproject)

        assert len(generators) == 1

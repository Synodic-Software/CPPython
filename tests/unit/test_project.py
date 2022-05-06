"""
Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

import logging

from cppython_core.schema import (
    PEP621,
    CPPythonData,
    Generator,
    GeneratorConfiguration,
    GeneratorData,
    PyProject,
    TargetEnum,
    ToolData,
)
from pytest_mock import MockerFixture

from cppython.project import Project, ProjectBuilder, ProjectConfiguration

default_pep621 = PEP621(name="test_name", version="1.0")
default_cppython_data = CPPythonData(**{"target": TargetEnum.EXE})
default_tool_data = ToolData(**{"cppython": default_cppython_data})
default_pyproject = PyProject(**{"project": default_pep621, "tool": default_tool_data})


class MockGeneratorData(GeneratorData):
    """
    TODO
    """

    check: bool


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
        Project(configuration, interface_mock, default_pyproject.dict(by_alias=True))


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

        generator_type = mocker.Mock()
        generator_type.name.return_value = "mock"
        generator_type.data_type.return_value = MockGeneratorData

        model_type = builder.generate_model([generator_type])

        project_data = default_pyproject.dict(by_alias=True)

        mock_data = MockGeneratorData(check=True)
        project_data["tool"]["cppython"]["mock"] = mock_data.dict(by_alias=True)
        result = model_type(**project_data)

        assert result.tool is not None
        assert result.tool.cppython is not None

        assert result.tool.cppython.mock.check

    def test_generator_creation(self, mocker: MockerFixture):
        """
        TODO
        """

        configuration = ProjectConfiguration()
        builder = ProjectBuilder(configuration)

        generator_configuration = GeneratorConfiguration()
        generators = builder.create_generators([], generator_configuration, default_pyproject)

        assert not generators

        generator = mocker.Mock()
        generators = builder.create_generators([generator], generator_configuration, default_pyproject)

        assert len(generators) == 1

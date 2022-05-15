"""
Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from pathlib import Path

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
        configuration = ProjectConfiguration(root_path=Path())
        Project(configuration, interface_mock, default_pyproject.dict(by_alias=True))


class TestBuilder:
    """
    TODO
    """

    def test_plugin_gather(self):
        """
        TODO
        """

        configuration = ProjectConfiguration(root_path=Path())
        builder = ProjectBuilder(configuration)
        plugins = builder.gather_plugins(Generator)

        assert len(plugins) == 0

    def test_generator_data_construction(self, mocker: MockerFixture):
        """
        TODO
        """

        configuration = ProjectConfiguration(root_path=Path())
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

        configuration = ProjectConfiguration(root_path=Path())
        builder = ProjectBuilder(configuration)

        generator_configuration = GeneratorConfiguration()
        generators = builder.create_generators([], generator_configuration, default_pep621, default_cppython_data)

        assert not generators

        generator = mocker.Mock()
        generators = builder.create_generators(
            [generator], generator_configuration, default_pep621, default_cppython_data
        )

        assert len(generators) == 1

    def test_presets(self, tmpdir):
        """
        TODO
        """

        configuration = ProjectConfiguration(root_path=Path())
        builder = ProjectBuilder(configuration)

        temporary_directory = Path(tmpdir)

        input_toolchain = temporary_directory / "input.cmake"

        with open(input_toolchain, "w", encoding="utf8") as file:
            file.write("")

        generator_output = [("test", input_toolchain)]
        builder.write_presets(temporary_directory, generator_output)

        cppython_tool = temporary_directory / "cppython"
        assert cppython_tool.exists()

        cppython_file = cppython_tool / "cppython.json"
        assert cppython_file.exists()

        test_tool = cppython_tool / "test"
        assert test_tool.exists()

        test_file = test_tool / "test.json"
        assert test_file.exists()

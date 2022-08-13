"""
Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from __future__ import annotations

from pathlib import Path

from cppython_core.schema import (
    PEP621,
    ConfigurePreset,
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
from cppython.utility import read_json, write_json

default_pep621 = PEP621(name="test_name", version="1.0")
default_cppython_data = CPPythonData(**{"target": TargetEnum.EXE})
default_tool_data = ToolData(**{"cppython": default_cppython_data})
default_pyproject = PyProject(**{"project": default_pep621, "tool": default_tool_data})


class MockGeneratorData(GeneratorData):
    """
    TODO
    """

    check: bool

    def resolve(self: MockGeneratorData, project_configuration: ProjectConfiguration) -> MockGeneratorData:
        return self


class ExtendedCPPython(CPPythonData):
    """
    TODO
    """

    mock: MockGeneratorData


class TestProject:
    """
    TODO
    """

    def test_construction(self, mocker: MockerFixture):
        """
        Test project construction on this project
        """

        interface_mock = mocker.MagicMock()
        configuration = ProjectConfiguration(pyproject_file=Path("pyproject.toml"), version="1.0.0")
        Project(configuration, interface_mock, default_pyproject.dict(by_alias=True))


class TestBuilder:
    """
    TODO
    """

    def test_plugin_gather(self):
        """
        TODO
        """

        configuration = ProjectConfiguration(pyproject_file=Path("pyproject.toml"), version="1.0.0")
        builder = ProjectBuilder(configuration)
        plugins = builder.gather_plugins(Generator)

        assert len(plugins) == 0

    def test_generator_data_construction(self, mocker: MockerFixture):
        """
        TODO
        """

        configuration = ProjectConfiguration(pyproject_file=Path("pyproject.toml"), version="1.0.0")
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
        assert result.tool.cppython.mock is not None
        assert result.tool.cppython.mock.check

    def test_generator_creation(self, mocker: MockerFixture):
        """
        TODO
        """

        configuration = ProjectConfiguration(pyproject_file=Path("pyproject.toml"), version="1.0.0")
        builder = ProjectBuilder(configuration)

        generator_configuration = GeneratorConfiguration(root_path=configuration.pyproject_file.parent)
        generators = builder.create_generators([], generator_configuration, default_pep621, default_cppython_data)

        assert not generators

        generator_type = mocker.Mock()
        generator_type.name.return_value = "mock"
        generator_type.data_type.return_value = MockGeneratorData

        mock_data = MockGeneratorData(check=True)
        extended_cppython_dict = default_cppython_data.dict(exclude_defaults=True)
        extended_cppython_dict["mock"] = mock_data
        extended_cppython = ExtendedCPPython(**extended_cppython_dict)

        generators = builder.create_generators(
            [generator_type],
            generator_configuration,
            default_pep621,
            extended_cppython,
        )

        assert len(generators) == 1

    def test_presets(self, tmp_path: Path):
        """
        TODO
        """

        # Write a dummy file for the config
        test_file = tmp_path / "pyproject.toml"
        test_file.write_text("Test File", encoding="utf-8")

        configuration = ProjectConfiguration(pyproject_file=test_file, version="1.0.0")
        builder = ProjectBuilder(configuration)

        input_toolchain = tmp_path / "input.cmake"

        with open(input_toolchain, "w", encoding="utf8") as file:
            file.write("")

        configure_preset = ConfigurePreset(name="test_preset", toolchainFile=str(input_toolchain))

        generator_output = [("test", configure_preset)]
        builder.write_presets(tmp_path, generator_output)

        cppython_tool = tmp_path / "cppython"
        assert cppython_tool.exists()

        cppython_file = cppython_tool / "cppython.json"
        assert cppython_file.exists()

        test_tool = cppython_tool / "test"
        assert test_tool.exists()

        test_file = test_tool / "test.json"
        assert test_file.exists()

    def test_root_unmodified(self, tmp_path: Path):
        """
        TODO
        """

        # Write a dummy file for the config
        test_file = tmp_path / "pyproject.toml"
        test_file.write_text("Test File", encoding="utf-8")
        configuration = ProjectConfiguration(pyproject_file=test_file, version="1.0.0")

        builder = ProjectBuilder(configuration)

        # TODO: Translate into reuseable testing data
        output = {
            "version": 4,
            "cmakeMinimumRequired": {"major": 3, "minor": 23, "patch": 1},
            "include": ["should/be/replaced/cppython.json"],
            "configurePresets": [
                {
                    "name": "default",
                    "inherits": ["cppython"],
                    "hidden": True,
                    "description": "Tests that generator isn't removed",
                    "generator": "Should exist",
                },
            ],
        }

        input_preset = tmp_path / "CMakePresets.json"
        write_json(input_preset, output)

        builder.write_root_presets(tmp_path / "test_location")

        data = read_json(input_preset)

        # TODO: Assert the differences affect nothing but what is written by the builder

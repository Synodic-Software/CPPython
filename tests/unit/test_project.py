"""Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cppython_core.schema import (
    PEP621,
    ConfigurePreset,
    CPPythonData,
    GeneratorConfiguration,
    ProjectConfiguration,
    PyProject,
)
from pytest_cppython.mock import MockGenerator, MockGeneratorData
from pytest_mock import MockerFixture

from cppython.builder import Builder
from cppython.project import Project
from cppython.utility import read_json, write_json
from tests.data.fixtures import CPPythonProjectFixtures


class ExtendedCPPython(CPPythonData):
    """_summary_

    Args:
        CPPythonData: _description_
    """

    mock: MockGeneratorData


class TestProject(CPPythonProjectFixtures):
    """_summary_

    Args:
        CPPythonProjectFixtures: _description_
    """

    def test_construction_without_plugins(
        self, mocker: MockerFixture, project: PyProject, project_configuration: ProjectConfiguration
    ) -> None:
        """_summary_

        Args:
            mocker: _description_
            project: _description_
            project_configuration: _description_
        """

        interface_mock = mocker.MagicMock()
        Project(project_configuration, interface_mock, project.dict(by_alias=True))

    def test_construction_with_plugins(
        self, mocker: MockerFixture, project_configuration: ProjectConfiguration, mock_project: dict[str, Any]
    ) -> None:
        """_summary_

        Args:
            mocker: _description_
            project_configuration: _description_
            mock_project: _description_
        """

        mocked_plugin_list = [MockGenerator]
        mocker.patch("cppython.builder.Builder.gather_plugins", return_value=mocked_plugin_list)

        interface_mock = mocker.MagicMock()
        Project(project_configuration, interface_mock, mock_project)


class TestBuilder(CPPythonProjectFixtures):
    """_summary_

    Args:
        CPPythonProjectFixtures: _description_
    """

    def test_plugin_gather(self, project_configuration: ProjectConfiguration) -> None:
        """_summary_

        Args:
            project_configuration: _description_
        """

        builder = Builder(project_configuration)
        plugins = builder.gather_plugins(MockGenerator)

        assert len(plugins) == 0

    def test_generator_data_construction(
        self, mocker: MockerFixture, project_configuration: ProjectConfiguration, project: PyProject
    ) -> None:
        """_summary_

        Args:
            mocker: _description_
            project_configuration: _description_
            project: _description_
        """

        builder = Builder(project_configuration)
        model_type = builder.generate_model([])

        assert model_type.__base__ == PyProject

        generator_type = mocker.Mock()
        generator_type.name.return_value = "mock"
        generator_type.data_type.return_value = MockGeneratorData

        model_type = builder.generate_model([generator_type])

        project_data = project.dict(by_alias=True)

        mock_data = MockGeneratorData()
        project_data["tool"]["cppython"]["mock"] = mock_data.dict(by_alias=True)
        result = model_type(**project_data)

        assert result.tool is not None
        assert result.tool.cppython is not None

    def test_generator_creation(
        self, mocker: MockerFixture, project_configuration: ProjectConfiguration, pep621: PEP621, cppython: CPPythonData
    ) -> None:
        """_summary_

        Args:
            mocker: _description_
            project_configuration: _description_
            pep621: _description_
            cppython: _description_
        """

        builder = Builder(project_configuration)

        generator_configuration = GeneratorConfiguration(root_directory=project_configuration.pyproject_file.parent)

        resolved = builder.generate_resolved_cppython_model([])
        generators = builder.create_generators(
            [],
            project_configuration,
            generator_configuration,
            (pep621.resolve(project_configuration), cppython.resolve(resolved, project_configuration)),
        )

        assert not generators

        generator_type = mocker.Mock()
        generator_type.name.return_value = "mock"
        generator_type.data_type.return_value = MockGeneratorData

        mock_data = MockGeneratorData()
        extended_cppython_dict = cppython.dict(exclude_defaults=True)
        extended_cppython_dict["mock"] = mock_data
        extended_cppython = ExtendedCPPython(**extended_cppython_dict)

        resolved = builder.generate_resolved_cppython_model([generator_type])

        generators = builder.create_generators(
            [generator_type],
            project_configuration,
            generator_configuration,
            (pep621.resolve(project_configuration), extended_cppython.resolve(resolved, project_configuration)),
        )

        assert len(generators) == 1

    def test_presets(self, tmp_path: Path) -> None:
        """_summary_

        Args:
            tmp_path: _description_
        """

        # Write a dummy file for the config
        test_file = tmp_path / "pyproject.toml"
        test_file.write_text("Test File", encoding="utf-8")

        configuration = ProjectConfiguration(pyproject_file=test_file, version="1.0.0")
        builder = Builder(configuration)

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

    def test_root_unmodified(self, tmp_path: Path) -> None:
        """_summary_

        Args:
            tmp_path: _description_
        """

        # Write a dummy file for the config
        test_file = tmp_path / "pyproject.toml"
        test_file.write_text("Test File", encoding="utf-8")
        configuration = ProjectConfiguration(pyproject_file=test_file, version="1.0.0")

        builder = Builder(configuration)

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

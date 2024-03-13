"""Tests the Project type"""

from pathlib import Path

import tomlkit
from cppython_core.schema import (
    CPPythonLocalConfiguration,
    PEP621Configuration,
    ProjectConfiguration,
    PyProject,
    ToolData,
)
from pytest import FixtureRequest
from pytest_cppython.mock.interface import MockInterface

from cppython.project import Project

pep621 = PEP621Configuration(name="test-project", version="0.1.0")


class TestProject:
    """Various tests for the project object"""

    def test_self_construction(self, request: FixtureRequest) -> None:
        """The project type should be constructable with this projects configuration

        Args:
            request: The pytest request fixture
        """

        # Use the CPPython directory as the test data
        file = request.config.rootpath / "pyproject.toml"
        project_configuration = ProjectConfiguration(pyproject_file=file, version=None)
        interface = MockInterface()

        pyproject_data = tomlkit.loads(file.read_text(encoding="utf-8"))
        project = Project(project_configuration, interface, pyproject_data)

        # Doesn't have the cppython table
        assert not project.enabled

    def test_missing_tool_table(self, tmp_path: Path) -> None:
        """The project type should be constructable without the tool table

        Args:
            tmp_path: Temporary directory for dummy data
        """

        file_path = tmp_path / "pyproject.toml"

        with open(file_path, "a", encoding="utf8") as file:
            file.write("")

        project_configuration = ProjectConfiguration(pyproject_file=file_path, version=None)
        interface = MockInterface()

        pyproject = PyProject(project=pep621)
        project = Project(project_configuration, interface, pyproject.model_dump(by_alias=True))

        assert not project.enabled

    def test_missing_cppython_table(self, tmp_path: Path) -> None:
        """The project type should be constructable without the cppython table

        Args:
            tmp_path: Temporary directory for dummy data
        """

        file_path = tmp_path / "pyproject.toml"

        with open(file_path, "a", encoding="utf8") as file:
            file.write("")

        project_configuration = ProjectConfiguration(pyproject_file=file_path, version=None)
        interface = MockInterface()

        tool_data = ToolData()
        pyproject = PyProject(project=pep621, tool=tool_data)
        project = Project(project_configuration, interface, pyproject.model_dump(by_alias=True))

        assert not project.enabled

    def test_default_cppython_table(self, tmp_path: Path) -> None:
        """The project type should be constructable with the default cppython table

        Args:
            tmp_path: Temporary directory for dummy data
        """

        file_path = tmp_path / "pyproject.toml"

        with open(file_path, "a", encoding="utf8") as file:
            file.write("")

        project_configuration = ProjectConfiguration(pyproject_file=file_path, version=None)
        interface = MockInterface()

        cppython_config = CPPythonLocalConfiguration()
        tool_data = ToolData(cppython=cppython_config)
        pyproject = PyProject(project=pep621, tool=tool_data)
        project = Project(project_configuration, interface, pyproject.model_dump(by_alias=True))

        assert project.enabled

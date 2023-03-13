"""Tests the Project type"""


from pathlib import Path

import tomlkit
from cppython_core.schema import ProjectConfiguration
from pytest import FixtureRequest
from pytest_cppython.mock.interface import MockInterface

from cppython.project import Project


class TestProject:
    """Various tests for the project object"""

    def test_default_construction(self, request: FixtureRequest) -> None:
        """The project type should be constructable without pyproject.toml support.
        The CPPython project uses a working pyproject.toml file, and this file is used as the test data

        Args:
            request: The pytest request fixture
        """

        # Use the CPPython directory as the test data
        file = request.config.rootpath / "pyproject.toml"
        project_configuration = ProjectConfiguration(pyproject_file=file, version=None)
        interface = MockInterface()

        pyproject_data = tomlkit.loads(file.read_text(encoding="utf-8"))
        project = Project(project_configuration, interface, pyproject_data)

        assert project

    def test_missing_project_table(self, tmp_path: Path) -> None:
        """The project type should be constructable without the top level table

        Args:
            tmp_path: Temporary directory for dummy data
        """

        file = tmp_path / "pyproject.toml"
        project_configuration = ProjectConfiguration(pyproject_file=file, version=None)
        interface = MockInterface()

        project = Project(project_configuration, interface, {})

        assert project

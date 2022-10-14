"""Project test fixtures for all cppython tests
"""

from typing import Any

import pytest
from cppython_core.schema import (
    CPPythonLocalConfiguration,
    PEP621Configuration,
    PyProject,
    ToolData,
)
from pytest_cppython.fixtures import CPPythonFixtures
from pytest_cppython.mock import MockGenerator, MockProvider


class CPPythonProjectFixtures(CPPythonFixtures):
    """Additional fixtures to help test projects"""

    @pytest.fixture(name="tool", scope="session")
    def fixture_tool(self, cppython_local_configuration: CPPythonLocalConfiguration) -> ToolData:
        """The tool data
        Args:
            cppython_local_configuration: The parameterized cppython table
        Returns:
            Wrapped CPPython data
        """
        return ToolData(cppython=cppython_local_configuration)

    @pytest.fixture(name="project")
    def fixture_project(self, tool: ToolData, pep621_configuration: PEP621Configuration) -> PyProject:
        """Parameterized construction of PyProject data
        Args:
            tool: The tool table with internal cppython data
            pep621_configuration: The project table
        Returns:
            All the data as one object
        """
        return PyProject(project=pep621_configuration, tool=tool)

    @pytest.fixture(name="project_with_mocks")
    def fixture_project_with_mocks(self, project: PyProject) -> dict[str, Any]:
        """Extension of the 'project' fixture with mock data attached
        Args:
            project: The input project
        Returns:
            All the data as a dictionary
        """
        mocked_pyproject = project.dict(by_alias=True)
        mocked_pyproject["tool"]["cppython"]["provider"][MockProvider.name()] = {}
        mocked_pyproject["tool"]["cppython"]["generator"][MockGenerator.name()] = {}
        return mocked_pyproject

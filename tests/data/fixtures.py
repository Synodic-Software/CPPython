"""Project test fixtures for all cppython tests
"""

from typing import Any

import pytest
from cppython_core.schema import PEP621, CPPythonData, PyProject, ToolData
from pytest_cppython.fixtures import CPPythonFixtures
from pytest_cppython.mock import MockProviderData


class CPPythonProjectFixtures(CPPythonFixtures):
    """Additional fixtures to help test projects"""

    @pytest.fixture(name="tool", scope="session")
    def fixture_tool(self, cppython: CPPythonData) -> ToolData:
        """The tool data

        Args:
            cppython: The parameterized cppython table

        Returns:
            Wrapped CPPython data
        """

        return ToolData(cppython=cppython)

    @pytest.fixture(name="project", scope="session")
    def fixture_project(self, tool: ToolData, pep621: PEP621) -> PyProject:
        """Parameterized construction of PyProject data

        Args:
            tool: The tool table with internal cppython data
            pep621: The project table

        Returns:
            All the data as one object
        """

        return PyProject(project=pep621, tool=tool)

    @pytest.fixture(name="mock_project", scope="session")
    def fixture_mock_project(self, project: PyProject) -> dict[str, Any]:
        """Extension of the 'project' fixture with mock data attached

        Args:
            project: The input project

        Returns:
            All the data as a dictionary
        """

        mocked_pyproject = project.dict(by_alias=True)
        mocked_pyproject["tool"]["cppython"]["mock"] = MockProviderData()

        return mocked_pyproject

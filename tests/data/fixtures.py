"""TODO
"""

from typing import Any

import pytest
from cppython_core.schema import PEP621, CPPythonData, PyProject, ToolData
from pytest_cppython.fixtures import CPPythonFixtures
from pytest_cppython.mock import MockProviderData


class CPPythonProjectFixtures(CPPythonFixtures):
    """_summary_

    Args:
        CPPythonFixtures: _description_

    Returns:
        _description_
    """

    @pytest.fixture(name="tool", scope="session")
    def fixture_tool(self, cppython: CPPythonData) -> ToolData:
        """_summary_

        Args:
            cppython: _description_

        Returns:
            _description_
        """

        return ToolData(cppython=cppython)

    @pytest.fixture(name="project", scope="session")
    def fixture_project(self, tool: ToolData, pep621: PEP621) -> PyProject:
        """_summary_

        Args:
            tool: _description_
            pep621: _description_

        Returns:
            _description_
        """

        return PyProject(project=pep621, tool=tool)

    @pytest.fixture(name="mock_project", scope="session")
    def fixture_mock_project(self, project: PyProject) -> dict[str, Any]:
        """_summary_

        Args:
            project: _description_

        Returns:
            _description_
        """

        mocked_pyproject = project.dict(by_alias=True)
        mocked_pyproject["tool"]["cppython"]["mock"] = MockProviderData()

        return mocked_pyproject

"""Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from __future__ import annotations

import pytest
from cppython_core.exceptions import PluginError
from cppython_core.schema import ProjectConfiguration, PyProject
from pytest_cppython.fixtures import CPPythonFixtures
from pytest_mock import MockerFixture

from cppython.project import Project


class TestProject(CPPythonFixtures):
    """Grouping for Project class testing"""

    def test_construction_without_plugins(
        self, mocker: MockerFixture, project: PyProject, project_configuration: ProjectConfiguration
    ) -> None:
        """Verification that no error is thrown and output is gracefully handled if no provider plugins are found

        Args:
            mocker: Mocking fixture for interface mocking
            project: PyProject data to construct with
            project_configuration: Temporary workspace for path resolution
        """

        interface_mock = mocker.MagicMock()
        with pytest.raises(PluginError):
            Project(project_configuration, interface_mock, project.dict(by_alias=True))

"""Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import Any

import pytest
from cppython_core.exceptions import PluginError
from cppython_core.schema import (
    CoreData,
    CPPythonLocalConfiguration,
    PEP621Configuration,
    ProjectConfiguration,
    PyProject,
)
from pytest_cppython.fixtures import CPPythonFixtures
from pytest_cppython.mock.generator import MockGenerator
from pytest_cppython.mock.provider import MockProvider
from pytest_mock import MockerFixture

from cppython.builder import Builder
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

    def test_construction_with_plugins(
        self, mocker: MockerFixture, project_configuration: ProjectConfiguration, project_with_mocks: dict[str, Any]
    ) -> None:
        """Verification of full construction with mock provider plugin

        Args:
            mocker: Mocking fixture for interface mocking
            project_configuration: Temporary workspace for path resolution
            project_with_mocks: PyProject data to construct with
        """

        mocked_provider_list = [MockProvider]
        mocker.patch("cppython.builder.Builder.discover_providers", return_value=mocked_provider_list)

        mocked_generator_list = [MockGenerator]
        mocker.patch("cppython.builder.Builder.discover_generators", return_value=mocked_generator_list)

        interface_mock = mocker.MagicMock()
        project_configuration.version = None
        Project(project_configuration, interface_mock, project_with_mocks)


class TestBuilder(CPPythonFixtures):
    """Tests of builder steps"""

    def test_core_data_version(self) -> None:
        """Test the SCM config error override. Validated data is already tested."""

        builder = Builder(getLogger())

        project_configuration = ProjectConfiguration(pyproject_file=Path("pyproject.toml"), version=None)
        pep621_configuration = PEP621Configuration(name="version-resolve-test", dynamic=["version"], version=None)
        cppython_configuration = CPPythonLocalConfiguration()

        core_data = builder.generate_core_data(project_configuration, pep621_configuration, cppython_configuration)

        assert core_data.pep621_data.version

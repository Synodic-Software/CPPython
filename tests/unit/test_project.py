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
from pytest_cppython.mock import MockGenerator, MockProvider
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

    def test_plugin_gather(self) -> None:
        """Verifies that discovery works with no results"""

        builder = Builder(getLogger())
        providers = builder.discover_providers()

        assert len(providers) == 0

        generators = builder.discover_generators()

        assert len(generators) == 0

        vcs = builder.discover_vcs()

        assert len(vcs) == 1

    def test_provider_creation(
        self,
        core_data: CoreData,
        project_with_mocks: dict[str, Any],
    ) -> None:
        """Test that providers can be created with the mock data available

        Args:
            core_data: TODO
            project_with_mocks: Local config
        """

        builder = Builder(getLogger())

        provider_configurations = project_with_mocks["tool"]["cppython"]["provider"]

        providers = builder.create_providers(
            [MockProvider],
            core_data,
            provider_configurations,
        )

        assert len(providers) == 1

    def test_generator_creation(
        self,
        core_data: CoreData,
        project_with_mocks: dict[str, Any],
    ) -> None:
        """Test that providers can be created with the mock data available

        Args:
            core_data: TODO
            project_with_mocks: Local config
        """

        builder = Builder(getLogger())

        generator_configurations = project_with_mocks["tool"]["cppython"]["generator"]

        assert builder.create_generator(
            [MockGenerator],
            core_data,
            generator_configurations,
        )

    def test_core_data_version(self) -> None:
        """Test the VCS config error override. Validated data is already tested."""

        builder = Builder(getLogger())

        project_configuration = ProjectConfiguration(pyproject_file=Path("pyproject.toml"), version=None)
        pep621_configuration = PEP621Configuration(name="version-resolve-test", dynamic=["version"], version=None)
        cppython_configuration = CPPythonLocalConfiguration()

        core_data = builder.generate_core_data(project_configuration, pep621_configuration, cppython_configuration)

        assert core_data.pep621_data.version

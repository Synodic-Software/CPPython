"""Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from __future__ import annotations

from logging import getLogger
from typing import Any

from cppython_core.schema import CoreData, ProjectConfiguration, PyProject
from pytest_cppython.mock import MockProvider
from pytest_mock import MockerFixture

from cppython.builder import Builder
from cppython.project import Project
from tests.data.fixtures import CPPythonProjectFixtures


class TestProject(CPPythonProjectFixtures):
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

        mocked_plugin_list = [MockProvider]
        mocker.patch("cppython.builder.Builder.discover_providers", return_value=mocked_plugin_list)

        interface_mock = mocker.MagicMock()
        Project(project_configuration, interface_mock, project_with_mocks)


class TestBuilder(CPPythonProjectFixtures):
    """Tests of builder steps"""

    def test_plugin_gather(self) -> None:
        """Verifies that provider discovery works with no results"""

        builder = Builder(getLogger())
        plugins = builder.discover_providers()

        assert len(plugins) == 0

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

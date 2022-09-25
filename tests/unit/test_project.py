"""Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from __future__ import annotations

from logging import getLogger
from typing import Any

from cppython_core.schema import (
    PEP621,
    CPPythonData,
    ProjectConfiguration,
    ProviderConfiguration,
    PyProject,
)
from pytest_cppython.mock import MockProvider, MockProviderData
from pytest_mock import MockerFixture

from cppython.builder import Builder
from cppython.project import Project
from tests.data.fixtures import CPPythonProjectFixtures


class ExtendedCPPython(CPPythonData):
    """_summary_

    Args:
        CPPythonData: _description_
    """

    mock: MockProviderData


class TestProject(CPPythonProjectFixtures):
    """_summary_

    Args:
        CPPythonProjectFixtures: _description_
    """

    def test_construction_without_plugins(
        self, mocker: MockerFixture, project: PyProject, workspace: ProjectConfiguration
    ) -> None:
        """_summary_

        Args:
            mocker: _description_
            project: _description_
            workspace: _description_
        """

        interface_mock = mocker.MagicMock()
        Project(workspace, interface_mock, project.dict(by_alias=True))

    def test_construction_with_plugins(
        self, mocker: MockerFixture, workspace: ProjectConfiguration, mock_project: dict[str, Any]
    ) -> None:
        """_summary_

        Args:
            mocker: _description_
            workspace: _description_
            mock_project: _description_
        """

        mocked_plugin_list = [MockProvider]
        mocker.patch("cppython.builder.Builder.discover_providers", return_value=mocked_plugin_list)

        interface_mock = mocker.MagicMock()
        Project(workspace, interface_mock, mock_project)


class TestBuilder(CPPythonProjectFixtures):
    """_summary_

    Args:
        CPPythonProjectFixtures: _description_
    """

    def test_plugin_gather(self, workspace: ProjectConfiguration) -> None:
        """_summary_

        Args:
            workspace: _description_
        """

        builder = Builder(workspace, getLogger())
        plugins = builder.discover_providers()

        assert len(plugins) == 0

    def test_provider_data_construction(
        self, mocker: MockerFixture, workspace: ProjectConfiguration, project: PyProject
    ) -> None:
        """_summary_

        Args:
            mocker: _description_
            workspace: _description_
            project: _description_
        """

        builder = Builder(workspace, getLogger())
        model_type = builder.generate_model([])

        assert model_type.__base__ == PyProject

        provider_type = mocker.Mock()
        provider_type.name.return_value = "mock"
        provider_type.data_type.return_value = MockProviderData

        model_type = builder.generate_model([provider_type])

        project_data = project.dict(by_alias=True)

        mock_data = MockProviderData()
        project_data["tool"]["cppython"]["mock"] = mock_data.dict(by_alias=True)
        result = model_type(**project_data)

        assert result.tool is not None
        assert result.tool.cppython is not None

    def test_provider_creation(
        self, mocker: MockerFixture, workspace: ProjectConfiguration, pep621: PEP621, cppython: CPPythonData
    ) -> None:
        """_summary_

        Args:
            mocker: _description_
            workspace: _description_
            pep621: _description_
            cppython: _description_
        """

        builder = Builder(workspace, getLogger())

        provider_configuration = ProviderConfiguration(root_directory=workspace.pyproject_file.parent)

        resolved = builder.generate_resolved_cppython_model([])

        provider_type = mocker.Mock()
        provider_type.name.return_value = "mock"
        provider_type.data_type.return_value = MockProviderData

        mock_data = MockProviderData()
        extended_cppython_dict = cppython.dict(by_alias=True)
        extended_cppython_dict["mock"] = mock_data
        extended_cppython = ExtendedCPPython(**extended_cppython_dict)

        resolved = builder.generate_resolved_cppython_model([provider_type])

        providers = builder.create_providers(
            [provider_type],
            workspace,
            provider_configuration,
            (pep621.resolve(workspace), extended_cppython.resolve(resolved, workspace)),
        )

        assert len(providers) == 1

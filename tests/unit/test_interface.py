"""Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

import pytest
from click.testing import CliRunner
from cppython_core.schema import PyProject
from pytest_cppython.plugin import InterfaceUnitTests
from pytest_mock.plugin import MockerFixture

from cppython.console.interface import Configuration, ConsoleInterface, cli
from cppython.schema import API
from tests.data.fixtures import CPPythonProjectFixtures


class TestCLIInterface(CPPythonProjectFixtures, InterfaceUnitTests[ConsoleInterface]):
    """The tests for our CLI interface"""

    @pytest.fixture(name="interface_type")
    def fixture_interface_type(self) -> type[ConsoleInterface]:
        """A required testing hook that allows type generation

        Returns:
            _description_
        """
        return ConsoleInterface

    # Grab the API methods and parameterize them for automatic testing of the entry_points
    method_list = [func for func in dir(API) if callable(getattr(API, func)) and not func.startswith("__")]

    @pytest.mark.parametrize("command", method_list)
    def test_command(self, command: str, mocker: MockerFixture, project: PyProject) -> None:
        """_summary_

        Args:
            command: _description_
            mocker: _description_
            project: _description_
        """
        # Patch the project initialization
        mocker.patch("cppython.project.Project.__init__", return_value=None)

        # Patch the reading of data
        mocker.patch("cppython.console.interface._create_pyproject", return_value=project)

        config = Configuration()

        # Patch out the implementation
        mocked_command = mocker.patch(f"cppython.project.Project.{command}")

        runner = CliRunner()
        result = runner.invoke(cli, [command], obj=config, catch_exceptions=False)

        assert result.exit_code == 0
        mocked_command.assert_called_once()

    def test_config(self) -> None:
        """_summary_"""

        Configuration()

    def test_verbosity(self) -> None:
        """_summary_"""

        config = Configuration()

        runner = CliRunner()
        result = runner.invoke(cli, "-v info", obj=config, catch_exceptions=False)

        assert result.exit_code == 0

        assert config.configuration.verbosity

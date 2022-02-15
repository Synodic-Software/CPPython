"""
Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

import pytest
from click.testing import CliRunner
from pytest_mock.plugin import MockerFixture

from cppython.plugins.interface.console import Config, ConsoleInterface, cli
from cppython.plugins.test.data import default_pyproject
from cppython.plugins.test.pytest import InterfaceUnitTests
from cppython.schema import API


class TestCLIInterface(InterfaceUnitTests):
    """
    The tests for our CLI interface
    """

    @pytest.fixture(name="interface")
    def fixture_interface(self) -> ConsoleInterface:
        """
        Override of the plugin provided interface fixture.

        Returns:
            ConsoleInterface -- The Interface object to use for the CPPython defined tests
        """
        return ConsoleInterface(default_pyproject)

    # Grab the API methods and parameterize them for automatic testing of the entry_points
    method_list = [func for func in dir(API) if callable(getattr(API, func)) and not func.startswith("__")]

    @pytest.mark.parametrize("command", method_list)
    def test_command(self, command: str, mocker: MockerFixture):
        """
        _summary_

        Arguments:
            command {str} -- The CLI command with the same name as the CPPython API call
            mocker {MockerFixture} -- pytest-mock fixture
        """
        # Patch the project initialization
        mocker.patch("cppython.project.Project.__init__", return_value=None)

        # Patch the reading of data
        mocker.patch("cppython.plugins.interface.console._create_pyproject", return_value=default_pyproject)

        config = Config()

        # Patch out the implementation
        mocked_command = mocker.patch(f"cppython.project.Project.{command}")

        runner = CliRunner()
        result = runner.invoke(cli, [command], obj=config, catch_exceptions=False)

        assert result.exit_code == 0
        mocked_command.assert_called_once()

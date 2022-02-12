"""
TODO:
"""

import pytest
from click.testing import CliRunner
from pytest_mock.plugin import MockerFixture

from cppython.plugins.interface.console import Config, ConsoleInterface, cli
from cppython.plugins.test.data import default_pyproject
from cppython.plugins.test.pytest import InterfaceUnitTests


class TestCLIInterface(InterfaceUnitTests):
    """
    The tests for our CLI interface
    """

    @pytest.fixture(name="interface")
    def fixture_interface(self):
        return ConsoleInterface(default_pyproject)

    @pytest.mark.parametrize("command", ["install", "update"])
    def test_command(self, command: str, mocker: MockerFixture):
        """
        TODO

        Arguments:
            interface {ConsoleInterface} -- [description]
            command {str} -- [description]
            mocker {[type]} -- [description]
        """
        # Patch the project initialization
        mocker.patch("cppython.project.Project.__init__", return_value=None)

        # Patch the reading of data
        mocker.patch("cppython.plugins.interface.console._create_pyproject", return_value=default_pyproject)

        config = Config()

        # Patch out the non-plugin implementation
        mocker.patch(f"cppython.project.Project.{command}")

        runner = CliRunner()
        result = runner.invoke(cli, [command], obj=config, catch_exceptions=False)

        assert result.exit_code == 0

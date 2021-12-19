import pytest
from click.testing import CliRunner

from cppython.plugins.interface.console import Config, ConsoleInterface, cli
from cppython.plugins.test.pytest import BaseInterface
from cppython.project import Project


@pytest.mark.parametrize("interface", [ConsoleInterface])
class TestCLIInterface(BaseInterface):
    """
    The tests for our CLI interface
    """

    @pytest.mark.parametrize("command", ["install", "update"])
    def test_command(self, interface, command, mocker):

        # Patch the project
        mocker.patch("cppython.plugins.interface.console.Config.load")

        # Patch the file IO
        mocker.patch("cppython.plugins.interface.console._read_data")

        config = Config()

        # Patch out the non-plugin implementation
        mocker.patch(f"cppython.project.Project.{command}")

        runner = CliRunner()
        result = runner.invoke(cli, [command], obj=config, catch_exceptions=False)

        assert result.exit_code == 0

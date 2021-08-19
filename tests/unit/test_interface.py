import pytest

from cppython.plugins.test.pytest import BaseInterface
from cppython.plugins.interface.console import ConsoleInterface, Config, cli

from click.testing import CliRunner


@pytest.mark.parametrize("interface", [ConsoleInterface])
class TestCLIInterface(BaseInterface):
    """
    The tests for our CLI interface
    """

    @pytest.mark.parametrize("command", ["install", "update"])
    def test_command(self, interface, command, mocker):

        # Pass in empty data
        obj = Config({})

        # Patch out the non-plugin implementation
        mocker.patch(f"config.project.{command}")

        runner = CliRunner()
        result = runner.invoke(cli, [command], obj=obj, catch_exceptions=False)

        assert result.exit_code == 0

"""Tests the click interface type"""

from click.testing import CliRunner

from cppython.console.interface import cli


class TestInterface:
    """Various tests for the click interface"""

    def test_info(self, cli_runner: CliRunner) -> None:
        """Verifies that the info command functions with CPPython hooks

        Args:
            cli_runner: The click runner
        """

        result = cli_runner.invoke(cli, ["info"], catch_exceptions=False)
        assert result.exit_code == 0

    def test_list(self, cli_runner: CliRunner) -> None:
        """Verifies that the list command functions with CPPython hooks

        Args:
            cli_runner: The click runner
        """

        result = cli_runner.invoke(cli, ["list"], catch_exceptions=False)
        assert result.exit_code == 0

    def test_update(self, cli_runner: CliRunner) -> None:
        """Verifies that the update command functions with CPPython hooks

        Args:
            cli_runner: The click runner
        """

        result = cli_runner.invoke(cli, ["update"], catch_exceptions=False)
        assert result.exit_code == 0

    def test_install(self, cli_runner: CliRunner) -> None:
        """Verifies that the install command functions with CPPython hooks

        Args:
            cli_runner: The click runner
        """

        result = cli_runner.invoke(cli, ["install"], catch_exceptions=False)
        assert result.exit_code == 0

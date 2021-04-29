from click.testing import CliRunner

from cppoetry.console import cli


class TestCLI:
    def test_validate(self, cli_workspace):
        result = cli_workspace.invoke(cli, ["validate"])

        if result.exception is not None:
            raise result.exception

    def test_install(self, cli_workspace):
        result = cli_workspace.invoke(cli, ["install"])

        if result.exception is not None:
            raise result.exception

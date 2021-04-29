from click.testing import CliRunner

from cppoetry.console import cli


class TestCLI:
    def test_validate(self, test_workspace):
        runner = CliRunner()

        with runner.isolated_filesystem():

            result = runner.invoke(cli, ["validate"])

            if result.exception is not None:
                raise result.exception

    def test_install(self, test_workspace):

        runner = CliRunner()

        with runner.isolated_filesystem():

            result = runner.invoke(cli, ["install"])

            if result.exception is not None:
                raise result.exception

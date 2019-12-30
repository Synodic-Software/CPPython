from conan_for_poetry.cli import entrypoint
from click.testing import CliRunner


class TestCLI():

    def test_cli_check(self):
        runner = CliRunner()
        result = runner.invoke(entrypoint, ['check'])
        assert result.exit_code == 0

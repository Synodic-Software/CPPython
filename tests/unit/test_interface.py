import pytest

from cppython.plugins.test.pytest import BaseInterface
from cppython.plugins.interface.console import ConsoleInterface, Config, cli

from click.testing import CliRunner


@pytest.mark.parametrize("interface", [ConsoleInterface])
class TestCLIInterface(BaseInterface):
    """
    The tests for our CLI interface
    """

    def test_install(self, interface):
        obj = Config()

        runner = CliRunner()
        result = runner.invoke(cli, ['install'], obj=obj, catch_exceptions=False)

        assert result.exit_code == 0

    def test_update(self, interface):
        obj = Config()

        runner = CliRunner()
        result = runner.invoke(cli, ['update'], obj=obj, catch_exceptions=False)

        assert result.exit_code == 0

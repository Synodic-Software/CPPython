import pytest

from cppython.plugins.test.pytest import BaseInterface
from cppython.plugins.interface.console import ConsoleInterface, install, update

from click.testing import CliRunner


@pytest.mark.parametrize("interface", [ConsoleInterface])
class TestCLIInterface(BaseInterface):
    """
    The tests for our CLI interface
    """

    def test_install(self):
        runner = CliRunner()
        result = runner.invoke(install)

        assert result.exit_code == 0

    def test_update(self):
        runner = CliRunner()
        result = runner.invoke(update)
        
        assert result.exit_code == 0

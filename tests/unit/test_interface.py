"""Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

import pytest
from click.testing import CliRunner
from pytest_cppython.plugin import InterfaceUnitTests

from cppython.console.interface import Configuration, ConsoleInterface, cli
from tests.data.fixtures import CPPythonProjectFixtures


class TestCLIInterface(CPPythonProjectFixtures, InterfaceUnitTests[ConsoleInterface]):
    """The tests for our CLI interface"""

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[ConsoleInterface]:
        """A required testing hook that allows type generation

        Returns:
            An overridden interface type
        """
        return ConsoleInterface

    def test_config(self) -> None:
        """Verify that the configuration object can be constructed"""

        Configuration()

    def test_verbosity(self) -> None:
        """Test that verbosity is passed through to the CLI"""

        config = Configuration()

        runner = CliRunner()
        result = runner.invoke(cli, "-v info", obj=config, catch_exceptions=False)

        assert result.exit_code == 0

        assert config.configuration.verbosity

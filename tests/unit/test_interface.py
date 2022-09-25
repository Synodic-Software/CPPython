"""Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

import pytest
from click.testing import CliRunner
from cppython_core.schema import ProjectConfiguration, PyProject
from pytest_cppython.plugin import InterfaceUnitTests
from pytest_mock.plugin import MockerFixture

from cppython.console.interface import Configuration, ConsoleInterface, cli
from cppython.project import Project
from cppython.schema import API
from tests.data.fixtures import CPPythonProjectFixtures


class TestCLIInterface(CPPythonProjectFixtures, InterfaceUnitTests[ConsoleInterface]):
    """The tests for our CLI interface"""

    @pytest.fixture(name="interface_type")
    def fixture_interface_type(self) -> type[ConsoleInterface]:
        """A required testing hook that allows type generation

        Returns:
            _description_
        """
        return ConsoleInterface

    def test_config(self) -> None:
        """_summary_"""

        Configuration()

    def test_verbosity(self) -> None:
        """_summary_"""

        config = Configuration()

        runner = CliRunner()
        result = runner.invoke(cli, "-v info", obj=config, catch_exceptions=False)

        assert result.exit_code == 0

        assert config.configuration.verbosity

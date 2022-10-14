"""Test the integrations related to the internal interface implementation and the 'Interface' interface itself
"""

import pytest
from pytest_cppython.plugin import InterfaceIntegrationTests

from cppython.console.interface import ConsoleInterface


class TestCLIInterface(InterfaceIntegrationTests[ConsoleInterface]):
    """The tests for our CLI interface"""

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[ConsoleInterface]:
        """A required testing hook that allows type generation

        Returns:
            An overridden interface type
        """
        return ConsoleInterface

"""Test the integrations related to the internal interface implementation and the 'Interface' interface itself
"""

import pytest
from pytest_cppython.plugin import InterfaceIntegrationTests

from cppython.console.interface import ConsoleInterface


class TestCLIInterface(InterfaceIntegrationTests[ConsoleInterface]):
    """The tests for our CLI interface"""

    @pytest.fixture(name="interface")
    def fixture_interface(self, interface_type: type[ConsoleInterface]) -> ConsoleInterface:
        """Override of the plugin provided interface fixture.

        Args:
            interface_type: The input interface type

        Returns:
            ConsoleInterface -- The Interface object to use for the CPPython defined tests
        """
        return ConsoleInterface()

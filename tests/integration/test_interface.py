"""Test the integrations related to the internal interface implementation and the 'Interface' interface itself
"""

import pytest
from cppython_core.schema import InterfaceConfiguration
from pytest_cppython.plugin import InterfaceIntegrationTests

from cppython.console.interface import ConsoleInterface


class TestCLIInterface(InterfaceIntegrationTests[ConsoleInterface]):
    """The tests for our CLI interface"""

    @pytest.fixture(name="interface")
    def fixture_interface(
        self, interface_type: type[ConsoleInterface], interface_configuration: InterfaceConfiguration
    ) -> ConsoleInterface:
        """Override of the plugin provided interface fixture.

        Args:
            interface_type: The input interface type
            interface_configuration: Interface configuration for construction

        Returns:
            ConsoleInterface -- The Interface object to use for the CPPython defined tests
        """
        configuration = InterfaceConfiguration()
        return ConsoleInterface(configuration)

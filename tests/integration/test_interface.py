"""
Test the integrations related to the internal interface implementation and the 'Interface' interface itself
"""

import pytest

from cppython.plugins.interface.console import ConsoleInterface
from cppython.plugins.test.data import default_pyproject
from cppython.plugins.test.pytest import InterfaceIntegrationTests


class TestCLIInterface(InterfaceIntegrationTests):
    """
    The tests for our CLI interface
    """

    @pytest.fixture(name="interface")
    def fixture_interface(self):
        """
        Override of the plugin provided interface fixture.

        Returns:
            ConsoleInterface -- The Interface object to use for the CPPython defined tests
        """
        return ConsoleInterface(default_pyproject)

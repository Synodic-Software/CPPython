"""
TODO:
"""

import pytest

from cppython.plugins.interface.console import ConsoleInterface
from cppython.plugins.test.pytest import InterfaceIntegrationTests


class TestCLIInterface(InterfaceIntegrationTests):
    """
    The tests for our CLI interface
    """

    @pytest.fixture(name="interface")
    def fixture_interface(self):
        return ConsoleInterface()

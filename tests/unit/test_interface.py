import pytest

from cppython.plugins.test.pytest import InterfaceSuite
from cppython.plugins.interface import console


@pytest.mark.parametrize("interface", [console])
class TestCLIInterface(InterfaceSuite):
    """
    The tests for our CLI interface
    """

    pass

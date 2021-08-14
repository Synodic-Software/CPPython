import pytest

from cppython.plugins.test.pytest import BaseInterface
from cppython.plugins.interface.console import ConsoleInterface


@pytest.mark.parametrize("interface", [ConsoleInterface])
class TestCLIInterface(BaseInterface):
    """
    The tests for our CLI interface
    """

    pass

import pytest

from cppython.plugins.test.pytest import GeneratorSuite
from cppython.plugins.generator import cmake


@pytest.mark.parametrize("generator", [cmake])
class TestCMakeGenerator(GeneratorSuite):
    """
    The tests for our CMake generator
    """

    pass
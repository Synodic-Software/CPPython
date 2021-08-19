import pytest

from cppython.plugins.test.pytest import BaseGenerator
from cppython.plugins.generator.cmake import CMakeGenerator


@pytest.mark.parametrize("generator", [CMakeGenerator])
class TestCMakeGenerator(BaseGenerator):
    """
    The tests for our CMake generator
    """

    def test_name(self, generator):
        """
        Tests that the generators name is expected
        """
        assert generator.name() == "cmake"

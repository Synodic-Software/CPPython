"""
TODO:
"""

import pytest

from cppython.plugins.generator.cmake import CMakeGenerator
from cppython.plugins.test.pytest import BaseGeneratorSuite


@pytest.mark.parametrize("generator", [CMakeGenerator])
class TestCMakeGenerator(BaseGeneratorSuite):
    """
    The tests for our CMake generator
    """

    def test_name(self, generator):
        """
        Tests that the generators name is expected
        """
        assert generator.name() == "cmake"

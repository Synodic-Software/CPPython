"""
TODO:
"""

from cppython.plugins.generator.cmake import CMakeGenerator
from cppython.plugins.test.pytest import BaseGeneratorSuite


class TestCMakeGenerator(BaseGeneratorSuite):
    """
    The tests for our CMake generator
    """

    def test_type(self, generator: CMakeGenerator):
        """
        Tests that the generators name is expected
        """
        assert generator.data_type == CMakeGenerator

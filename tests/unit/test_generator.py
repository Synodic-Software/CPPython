"""
TODO:
"""

from cppython.plugins.generator.cmake import CMakeData, CMakeGenerator
from cppython.plugins.test.pytest import BaseGeneratorSuite


class TestCMakeGenerator(BaseGeneratorSuite):
    """
    The tests for our CMake generator
    """

    def __init__(self) -> None:
        super().__init__(CMakeGenerator, CMakeData)

    def test_type(self, generator: CMakeGenerator):
        """
        Tests that the generators name is expected
        """
        assert generator.data_type == CMakeGenerator

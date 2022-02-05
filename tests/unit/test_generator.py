"""
TODO:
"""

import pytest

from cppython.plugins.generator.cmake import CMakeData, CMakeGenerator
from cppython.plugins.test.data import default_metadata, default_pep621
from cppython.plugins.test.pytest import BaseGeneratorSuite


class TestCMakeGenerator(BaseGeneratorSuite):
    """
    The tests for our CMake generator
    """

    @pytest.fixture(name="generator")
    def fixture_generator(self):
        cmake_data = CMakeData()
        return CMakeGenerator(default_pep621, default_metadata, cmake_data)

    def test_type(self, generator: CMakeGenerator):
        """
        Tests that the generators name is expected
        """
        assert generator.data_type == CMakeGenerator

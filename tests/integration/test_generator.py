"""
TODO:
"""

import pytest

from cppython.plugins.generator.cmake import CMakeData, CMakeGenerator
from cppython.plugins.test.data import default_pyproject
from cppython.plugins.test.pytest import GeneratorIntegrationTests


class TestCMakeGenerator(GeneratorIntegrationTests):
    """
    The tests for our CMake generator
    """

    @pytest.fixture(name="generator")
    def fixture_generator(self):
        cmake_data = CMakeData()
        return CMakeGenerator(default_pyproject, cmake_data)

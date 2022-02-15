"""
Test the integrations related to the internal generator implementation and the 'Generator' interface itself
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
        """
        Override of the plugin provided generator fixture.

        Returns:
            CMakeGenerator -- The Generator object to use for the CPPython defined tests
        """
        cmake_data = CMakeData()
        return CMakeGenerator(default_pyproject, cmake_data)

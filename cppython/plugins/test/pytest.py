"""
TODO:
"""
from abc import ABC
from importlib.metadata import entry_points

import pytest

from cppython.schema import Generator, Interface


class BaseGeneratorSuite(ABC):
    """
    Custom implementations of the Generator class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

    @pytest.fixture(name="generator")
    def fixture_generator(self) -> Generator:
        """
        A hook allowing implementations to override the fixture with a parameterization
            @pytest.mark.parametrize("generator", [CustomGenerator])
        """
        raise NotImplementedError

    def test_plugin_registration(self, generator: Generator):
        """
        TODO
        """
        plugin_entries = entry_points(group=f"cppython.{generator.plugin_group()}")
        assert len(plugin_entries) > 0


class BaseInterfaceSuite(ABC):
    """
    Custom implementations of the Interface class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

    @pytest.fixture(name="interface")
    def fixture_interface(self) -> Interface:
        """
        A hook allowing implementations to override the fixture with a parameterization
            @pytest.mark.parametrize("interface", [CustomInterface])
        """
        raise NotImplementedError

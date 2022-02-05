"""
TODO:
"""
from abc import ABC

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

    def test_construction(self, generator: Generator):
        """
        Test the __init__ call of the generator object
        """
        pass


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

    def test_construction(self, interface: Interface):
        """
        Test the __init__ call of the interface object
        """

"""
TODO:
"""
from abc import ABC
from typing import Type

import pytest

from cppython.schema import Generator, Interface


class BaseGeneratorSuite(ABC):
    """
    Custom implementations of the Generator class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

    @pytest.fixture
    def generator(self) -> Type[Generator]:
        """
        A hook allowing implementations to override the fixture with a parameterization
            @pytest.mark.parametrize("generator", [CustomGenerator])
        """
        raise NotImplementedError

    def test_construction(self):
        """
        Test the __init__ call of the generator object
        """
        self.generator()


class BaseInterfaceSuite(ABC):
    """
    Custom implementations of the Interface class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

    @pytest.fixture
    def interface(self) -> Type[Interface]:
        """
        A hook allowing implementations to override the fixture with a parameterization
            @pytest.mark.parametrize("interface", [CustomInterface])
        """
        raise NotImplementedError

    def test_construction(self):
        """
        Test the __init__ call of the interface object
        """
        self.interface()

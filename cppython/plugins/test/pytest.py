"""
TODO:
"""
from abc import ABC
from typing import Type

import pytest

from cppython.schema import Generator, Interface


@pytest.fixture
def generator() -> Type[Generator]:
    """
    A hook allowing implementations to override the fixture with a parameterization
        @pytest.mark.parametrize("generator", [CustomGenerator])
    """
    raise NotImplementedError


class BaseGeneratorSuite(ABC):
    """
    Custom implementations of the Generator class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

    def test_construction(self, generator):
        """
        Test the __init__ call of the generator object
        """
        generator()


@pytest.fixture
def interface() -> Interface:
    """
    A hook allowing implementations to override the fixture with a parameterization
        @pytest.mark.parametrize("interface", [CustomInterface])
    """
    raise NotImplementedError


class BaseInterfaceSuite(ABC):
    """
    Custom implementations of the Interface class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

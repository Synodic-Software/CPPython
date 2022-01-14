"""
TODO:
"""
from abc import ABC, abstractmethod
from typing import Type

import pytest

from cppython.schema import Generator, Interface


class BaseGeneratorSuite(ABC):
    """
    Custom implementations of the Generator class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

    @abstractmethod
    def __init__(self, generator_type: Type[Generator]) -> None:
        super().__init__()

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

    def test_construction(self, interface):
        """
        Test the __init__ call of the interface object
        """
        interface()

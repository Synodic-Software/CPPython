"""
TODO:
"""
from abc import ABC

import pytest


@pytest.fixture
def generator_type():
    """
    A hook allowing implementations to override the fixture with a parameterization
        @pytest.mark.parametrize("generator_type", [CustomGenerator])
    """
    raise NotImplementedError


@pytest.fixture
def generator(generator_type):
    """
    TODO:
    """
    return generator_type()


class BaseGenerator(ABC):
    """
    Custom implementations of the Generator class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

    def test_construction(self, generator_type):
        """
        Test the __init__ call of the generator object
        """
        generator_type()


@pytest.fixture
def interface_type():
    """
    A hook allowing implementations to override the fixture with a parameterization
        @pytest.mark.parametrize("interface_type", [CustomInterface])
    """
    raise NotImplementedError


@pytest.fixture
def interface(interface_type):
    """
    A hook allowing implementations to override the fixture with a parameterization
        @pytest.mark.parametrize("interface", [CustomInterface])
    """
    return interface_type()


class BaseInterface(ABC):
    """
    Custom implementations of the Interface class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

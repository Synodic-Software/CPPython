"""
TODO:
"""
from abc import ABC

import pytest


@pytest.fixture
def generator():
    """
    A hook allowing implementations to override the fixture with a parameterization
        @pytest.mark.parametrize("generator", [CustomGenerator])
    """
    raise NotImplementedError


class BaseGenerator(ABC):
    """
    Custom implementations of the Generator class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

    def test_construction(self):
        """
        Test the __init__ call of the generator object
        """
        pass


@pytest.fixture
def interface():
    """
    A hook allowing implementations to override the fixture with a parameterization
        @pytest.mark.parametrize("interface", [CustomInterface])
    """
    raise NotImplementedError


class BaseInterface(ABC):
    """
    Custom implementations of the Interface class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

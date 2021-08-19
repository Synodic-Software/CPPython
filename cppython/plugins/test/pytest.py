import pytest


@pytest.fixture
def generator():
    """
    A hook allowing implementations to override the fixture with a parameterization
    """
    raise NotImplementedError


class BaseGenerator:
    """
    Implementations of the Generator class should inherit from this class for its tests
    """

    pass


@pytest.fixture
def interface():
    """
    A hook allowing implementations to override the fixture with a parameterization
    """
    raise NotImplementedError


class BaseInterface:
    """
    Implementations of the Interface class should inherit from this class for its tests
    """

    pass

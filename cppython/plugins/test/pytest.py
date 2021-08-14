import pytest


@pytest.fixture
def generator():
    raise NotImplementedError


class BaseGenerator:
    def test_todo(self, generator):
        pass


@pytest.fixture
def interface():
    raise NotImplementedError


class BaseInterface:
    def test_todo(self, interface):
        pass

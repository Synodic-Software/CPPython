import pytest


@pytest.fixture
def generator():
    raise NotImplementedError


class GeneratorSuite:
    def test_todo(self, generator):
        pass


@pytest.fixture
def interface():
    raise NotImplementedError


class InterfaceSuite:
    def test_todo(self, interface):
        pass

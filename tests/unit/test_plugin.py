import pytest

from pathlib import Path


# Fixtures
@pytest.fixture
def plugin_workspace(test_workspace: Path):
    """
    @returns - 
    """

    return test_workspace


# Tests
class TestPlugin:
    def test_validate(self, plugin_workspace):
        pass

    def test_install(self, plugin_workspace):
        pass

    def test_update(self, plugin_workspace):
        pass
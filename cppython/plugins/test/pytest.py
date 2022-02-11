"""
TODO:
"""
from abc import ABC
from importlib.metadata import entry_points

import pytest

from cppython.project import Project
from cppython.schema import Generator, Interface


class GeneratorTests(ABC):
    """
    TODO
    """

    @pytest.fixture(name="generator")
    def fixture_generator(self) -> Generator:
        """
        A hook allowing implementations to override the fixture with a parameterization
            @pytest.mark.parametrize("generator", [CustomGenerator])
        """
        raise NotImplementedError


class GeneratorIntegrationTests(GeneratorTests):
    """
    TODO
    """

    def test_plugin_registration(self, generator: Generator):
        """
        TODO
        """
        plugin_entries = entry_points(group=f"cppython.{generator.plugin_group()}")
        assert len(plugin_entries) > 0


class GeneratorUnitTests(GeneratorTests):
    """
    Custom implementations of the Generator class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

    def test_name(self, generator: Generator):
        """
        TODO
        """
        name = generator.name()

        assert name != ""

    def test_data_type(self, generator: Generator):
        """
        TODO
        """
        data_type = generator.data_type()

        assert data_type != ""


class InterfaceTests(ABC):
    """
    TODO
    """

    @pytest.fixture(name="interface")
    def fixture_interface(self) -> Interface:
        """
        A hook allowing implementations to override the fixture with a parameterization
            @pytest.mark.parametrize("interface", [CustomInterface])
        """
        raise NotImplementedError


class InterfaceIntegrationTests(InterfaceTests):
    """
    TODO
    """

    def test_project(self, interface: Interface):
        """
        TODO
        """
        Project(interface)


class InterfaceUnitTests(InterfaceTests):
    """
    Custom implementations of the Interface class should inherit from this class for its tests.
    This class provides a generic test suite that all custom types must function with.
    """

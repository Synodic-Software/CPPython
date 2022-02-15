"""
Helper fixtures and plugin definitions for pytest
TODO: Should by a pytest plugin, removing the need for this module in production code.
"""
from abc import ABC
from importlib.metadata import entry_points

import pytest

from cppython.project import Project
from cppython.schema import Generator, Interface


class GeneratorTests(ABC):
    """
    Shared functionality between the different Generator testing categories
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
    Base class for all generator integration tests that test plugin agnostic behavior
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
    Base class for all generator unit tests that test plugin agnostic behavior
    """

    def test_name(self, generator: Generator):
        """
        Test name restrictions
        TODO: This should be a pydantic schema
        """
        name = generator.name()

        assert name != ""

    def test_data_type(self, generator: Generator):
        """
        Test data_type restrictions
        TODO: This should be a pydantic schema
        """
        data_type = generator.data_type()

        assert data_type != ""


class InterfaceTests(ABC):
    """
    Shared functionality between the different Interface testing categories
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
    Base class for all interface integration tests that test plugin agnostic behavior
    """

    def test_project(self, interface: Interface):
        """
        Test that the project can be constructed from the given interface
        """
        Project(interface)


class InterfaceUnitTests(InterfaceTests):
    """
    Custom implementations of the Interface class should inherit from this class for its tests.
    Base class for all interface unit tests that test plugin agnostic behavior
    """

"""
The central delegation of the CPPython project
"""

from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Any, Type, TypeVar
from xmlrpc.client import Boolean

from cppython_core.schema import (
    API,
    CPPythonData,
    Generator,
    Interface,
    Plugin,
    PyProject,
    ToolData,
)
from pydantic import create_model


@dataclass
class ProjectConfiguration:
    """
    TODO
    """

    verbose: Boolean = False


class ProjectBuilder:
    """
    TODO
    """

    def __init__(self, configuration: ProjectConfiguration) -> None:
        self.configuration = configuration

    DerivedPlugin = TypeVar("DerivedPlugin", bound=Plugin)

    def gather_plugins(self, plugin_type: Type[DerivedPlugin]) -> list[Type[DerivedPlugin]]:
        """
        TODO
        """
        plugins = []
        entry_points = metadata.entry_points(group=f"cppython.{plugin_type.plugin_group()}")

        for entry_point in entry_points:
            loaded_plugin_type = entry_point.load()
            if issubclass(loaded_plugin_type, plugin_type) & (loaded_plugin_type is not plugin_type):
                plugins.append(loaded_plugin_type)

        return plugins

    def generate_model(self, plugins: list[Type[Generator]]) -> Type[PyProject]:
        """
        TODO: Proper return type hint
        """
        plugin_fields = {}
        for plugin_type in plugins:
            plugin_fields[plugin_type.name()] = (plugin_type.data_type(), ...)

        extended_cppython_type = create_model(
            "ExtendedCPPythonData",
            **plugin_fields,
            __base__=CPPythonData,
        )

        extended_tool_type = create_model(
            "ExtendedToolData",
            cppython=(extended_cppython_type, ...),
            __base__=ToolData,
        )

        return create_model(
            "ExtendedPyProject",
            tool=(extended_tool_type, ...),
            __base__=PyProject,
        )

    def create_generators(self, plugins: list[Type[Generator]], pyproject: PyProject) -> list[Generator]:
        """
        TODO
        """
        _generators = []
        for plugin_type in plugins:
            _generators.append(plugin_type(pyproject))

        return _generators


class Project(API):
    """
    The object constructed at each entry_point
    """

    def __init__(
        self, configuration: ProjectConfiguration, interface: Interface, pyproject_data: dict[str, Any]
    ) -> None:

        self.configuration = configuration

        if self.configuration.verbose:
            interface.print("Starting CPPython project initialization")

        builder = ProjectBuilder(self.configuration)
        plugins = builder.gather_plugins(Generator)

        if not plugins:
            if self.configuration.verbose:
                interface.print("No generator plugin was found.")
            return

        extended_pyproject_type = builder.generate_model(plugins)
        self.pyproject = extended_pyproject_type(**pyproject_data)

        if self.pyproject.tool is None:
            if self.configuration.verbose:
                interface.print("Table [tool] is not defined")
            return

        if self.pyproject.tool.cppython is None:
            if self.configuration.verbose:
                interface.print("Table [tool.cppython] is not defined")
            return

        self._interface = interface
        self._generators = builder.create_generators(plugins, self.pyproject)

        if self.configuration.verbose:
            interface.print("CPPython project initialized")

    def download(self, path: Path):
        """
        Download the generator tooling if required
        """

        for generator in self._generators:

            if not generator.generator_downloaded(path):
                self._interface.print(f"Downloading the {generator.name()} tool")

                # TODO: Make async with progress bar
                generator.download_generator(path)
                self._interface.print("Download complete")

    # API Contract

    def install(self) -> None:
        if self.pyproject.tool and self.pyproject.tool.cppython:
            if self.configuration.verbose:
                self._interface.print("CPPython: Installing...")
            self.download(self.pyproject.tool.cppython.install_path)

            for generator in self._generators:
                generator.install()

    def update(self) -> None:
        if self.pyproject.tool and self.pyproject.tool.cppython:
            if self.configuration.verbose:
                self._interface.print("CPPython: Updating...")

            for generator in self._generators:
                generator.update()

    def build(self) -> None:
        if self.pyproject.tool and self.pyproject.tool.cppython:
            if self.configuration.verbose:
                self._interface.print("CPPython: Building...")

            for generator in self._generators:
                generator.build()

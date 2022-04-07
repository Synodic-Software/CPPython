"""
The central delegation of the CPPython project
"""

from dataclasses import dataclass
from importlib import metadata
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

PluginType = TypeVar("PluginType", bound=Type[Plugin])


def gather_plugins(plugin_type: PluginType) -> list[Type[PluginType]]:
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


@dataclass
class ProjectConfiguration:
    """
    TODO
    """

    verbose: Boolean = False


class Project(API):
    """
    The object constructed at each entry_point
    """

    def __init__(
        self, configuration: ProjectConfiguration, interface: Interface, pyproject_data: dict[str, Any]
    ) -> None:

        self.enabled = False
        self.verbose = configuration.verbose

        if self.verbose:
            interface.print("Starting CPPython project initialization")

        # Gather
        plugins = gather_plugins(Generator)

        if not plugins:
            if self.verbose:
                interface.print("No generator plugin was found.")
            return

        plugin_fields = {}
        for plugin_type in plugins:
            plugin_fields[plugin_type.name()] = plugin_type.data_type()

        ExtendedCPPythonData = create_model(
            "ExtendedCPPythonData",
            **plugin_fields,
            __base__=CPPythonData,
        )

        ExtendedToolData = create_model(
            "ToolData",
            cppython=ExtendedCPPythonData,
            __base__=ToolData,
        )

        pyproject = PyProject(**pyproject_data)

        if pyproject.tool is None:
            if self.verbose:
                interface.print("Table [tool] is not defined")
            return

        if pyproject.tool.cppython is None:
            if self.verbose:
                interface.print("Table [tool.cppython] is not defined")
            return

        self.enabled = True

        self._interface = interface

        self._generators = []
        for plugin_type in plugins:
            self._generators.append(plugin_type(pyproject))

        if self.verbose:
            interface.print("CPPython project initialized")

    def download(self):
        """
        Download the generator tooling if required
        """
        for generator in self._generators:

            if not generator.generator_downloaded():
                self._interface.print(f"Downloading the {generator.name()} tool")

                # TODO: Make async with progress bar
                generator.download_generator()
                self._interface.print("Download complete")

    # API Contract

    def install(self) -> None:
        if self.enabled:
            if self.verbose:
                self._interface.print("CPPython: Installing...")
            self.download()

            for generator in self._generators:
                generator.install()

    def update(self) -> None:
        if self.enabled:
            if self.verbose:
                self._interface.print("CPPython: Updating...")

            for generator in self._generators:
                generator.update()

    def build(self) -> None:
        if self.enabled:
            if self.verbose:
                self._interface.print("CPPython: Building...")

            for generator in self._generators:
                generator.build()

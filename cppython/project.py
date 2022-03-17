"""
The central delegation of the CPPython project
"""

from dataclasses import dataclass
from importlib import metadata
from typing import Callable, Optional, Type, TypeVar
from xmlrpc.client import Boolean

from cppython_core.exceptions import ConfigError
from cppython_core.schema import API, Generator, Interface, Plugin, PyProject


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

    def __init__(self, configuration: ProjectConfiguration, interface: Interface, pyproject: PyProject) -> None:

        self.enabled = False
        self.verbose = configuration.verbose

        if self.verbose:
            interface.print("Starting CPPython project initialization")

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

        PluginType = TypeVar("PluginType", bound=Type[Plugin])

        def find_plugin_type(plugin_type: PluginType, condition: Callable[[str], bool]) -> Optional[PluginType]:
            """
            Finds the first plugin that satisfies the given condition
            """

            entry_points = metadata.entry_points(group=f"cppython.{plugin_type.plugin_group()}")

            for entry_point in entry_points:
                loaded_plugin_type = entry_point.load()
                if issubclass(loaded_plugin_type, plugin_type) & (loaded_plugin_type is not plugin_type):
                    if condition(loaded_plugin_type.name()):
                        return loaded_plugin_type

            return None

        plugin_type = find_plugin_type(Generator, lambda name: name == pyproject.tool.cppython.generator)

        if plugin_type is None:
            raise ConfigError(f"No generator plugin with the name '{pyproject.tool.cppython.generator}' was found.")

        generator_data = interface.read_generator_data(plugin_type.data_type())
        self._generator = plugin_type(pyproject, generator_data)

        if self.verbose:
            interface.print("CPPython project initialized")

    def download(self):
        """
        Download the generator tooling if required
        """
        if not self._generator.generator_downloaded():
            self._interface.print(f"Downloading the {self._generator.name()} tool")

            # TODO: Make async with progress bar
            self._generator.download_generator()
            self._interface.print("Download complete")

    # API Contract

    def install(self) -> None:
        if self.enabled:
            if self.verbose:
                self._interface.print("CPPython: Installing...")
            self.download()
            self._generator.install()

    def update(self) -> None:
        if self.enabled:
            if self.verbose:
                self._interface.print("CPPython: Updating...")
            self._generator.update()

    def build(self) -> None:
        if self.enabled:
            if self.verbose:
                self._interface.print("CPPython: Building...")
            self._generator.build()

"""
The central delegation of the CPPython project
"""

from importlib import metadata
from typing import Callable, Optional, Type, TypeVar

from cppython.exceptions import ConfigError
from cppython.schema import API, Generator, Interface, Plugin


class Project(API):
    """
    The object constructed at each entry_point
    """

    def __init__(self, interface: Interface) -> None:

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

        plugin_type = find_plugin_type(Generator, lambda name: name == interface.pyproject.cppython_data.generator)

        if plugin_type is None:
            raise ConfigError(
                f"No generator plugin with the name '{interface.pyproject.cppython_data.generator}' was found."
            )

        generator_data = interface.read_generator_data(plugin_type.data_type())
        self._generator = plugin_type(interface.pyproject, generator_data)
        self._generator.install_generator()

    # API Contract

    def install(self) -> None:
        self._generator.install()

    def update(self) -> None:
        self._generator.update()

    def build(self) -> None:
        self._generator.build()

from typing import Type, Callable

from cppython.schema import API, Interface, Generator, Metadata, Plugin
from cppython.exceptions import ConfigError

import pkgutil
import importlib
import inspect


class Project(API):
    def __init__(self, interface_type: Type[Interface]) -> None:

        # Construct the interface
        self._interface = interface_type()
        pyproject_data = self._interface.read_pyproject()

        # Each plugin reads its own configuration file, interfaces without external data need a helping hand parsing it
        if not interface_type.external_config():
            """
            If the interface doesn't support an external configuration, search for a plugin that does
            """

            temporary_interface_type = self._load_interface([*pyproject_data["tool"]])

            if temporary_interface_type is None:
                raise ConfigError("")

            pep_612 = temporary_interface_type.parse_pep_612(pyproject_data)

        else:
            pep_612 = self._interface.pep_612()

        # Remove the unnecessary data
        cppython_data = self._parse_cppython_data(pyproject_data)

        # Load the generator type
        generator_type = self._load_generator(cppython_data.generator)

        if generator_type is None:
            raise ConfigError("")

        # Pull out the raw generator specific data
        generator_data = cppython_data[cppython_data.generator]

        # Construct the generator
        self._generator = generator_type(pep_612, cppython_data, generator_data)

    def _parse_cppython_data(self, data: dict) -> Metadata:
        return Metadata(**data["tool"]["cppython"])

    def _find_first_plugin(self, namespace_package, plugin_type: Type[Plugin], condition: Callable[[str], bool]) -> Type[Plugin]:
        """
        Finds the first plugin that satisfies the given condition
        """
        for _, name, is_package in pkgutil.iter_modules(namespace_package.__path__, namespace_package.__name__ + "."):
            if not is_package:
                module = importlib.import_module(name)
                class_members = inspect.getmembers(module, inspect.isclass)
                for (_, value) in class_members:
                    if issubclass(value, plugin_type) & (value is not plugin_type):
                        if condition(value.name()):
                            return value

    def _load_interface(self, potential_keys: list) -> Type[Interface]:
        """
        TODO:
        """

        import cppython.plugins.interface

        return self._find_first_plugin(cppython.plugins.interface, Interface, lambda name : name in potential_keys)

    def _load_generator(self, generator: str) -> Type[Generator]:
        """
        TODO:
        """

        import cppython.plugins.generator

        return self._find_first_plugin(cppython.plugins.generator, Generator, lambda name : name == generator)

    """
    API Contract
    """

    def install(self) -> None:
        self._generator.install()

    def update(self) -> None:
        self._generator.update()

    def build(self) -> None:
        self._generator.build()

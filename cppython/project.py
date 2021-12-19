import importlib
import inspect
import pkgutil
from typing import Callable, Type

from cppython.exceptions import ConfigError
from cppython.schema import API, PEP621, Generator, Interface, Metadata, Plugin


class Project(API):
    def __init__(self, interface: Interface) -> None:

        self._interface = interface
        self.loaded = False

    def _parse_PEP621_data(self, data: dict, interface_type: Interface) -> PEP621:
        """
        Extracts the PEP621 metadata from the various possible project formats
        """

        # Each plugin reads its own configuration file, interfaces without external data need a helping hand parsing it
        if not interface_type.external_config():
            # If the interface doesn't support an external configuration, search for a plugin that does

            temporary_interface_type = self._load_interface([*data["tool"]])

            if temporary_interface_type is None:
                # If there is no applicable plugin, we are interfaceing the toml project without a python buildsystem

                return self._interface.pep_621()

            return temporary_interface_type.parse_pep_621(data)

        else:
            return self._interface.pep_621()

    def _parse_cppython_data(self, data: dict) -> Metadata:
        """
        TODO:
        """
        return Metadata(**data["tool"]["cppython"])

    def _parse_generator_data(self, data: dict, generator_type):
        """
        TODO:
        """
        generator_config_type = generator_type.data_type()
        return generator_config_type(**data[generator_type.name()])

    def _find_first_plugin(
        self, namespace_package, plugin_type: Type[Plugin], condition: Callable[[str], bool]
    ) -> Type[Plugin]:
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

        return self._find_first_plugin(cppython.plugins.interface, Interface, lambda name: name in potential_keys)

    def _load_generator(self, generator: str) -> Type[Generator]:
        """
        TODO:
        """

        import cppython.plugins.generator

        return self._find_first_plugin(cppython.plugins.generator, Generator, lambda name: name == generator)

    def load(self):
        # Read the raw configuration data
        pyproject_data = self._interface.read_pyproject()
        cppython_data = self._parse_cppython_data(pyproject_data)

        # Load the generator type
        generator_type = self._load_generator(cppython_data.generator)

        if generator_type is None:
            raise ConfigError("")

        pep_621 = self._parse_PEP621_data(pyproject_data, self._interface)
        generator_data = self._parse_generator_data(pyproject_data, generator_type)

        # Construct the generator
        self._generator = generator_type(pep_621, cppython_data, generator_data)

        self.loaded = True

    # API Contract

    def install(self) -> None:
        self._generator.install()

    def update(self) -> None:
        self._generator.update()

    def build(self) -> None:
        self._generator.build()

from pathlib import Path

from cppython.schema import API, Interface, Generator

import cppython.plugins.generator
import cppython.plugins.interface

import pkgutil
import importlib
import inspect
import cmake

class Project(API):
    def __init__(self, path: Path) -> None:
        """
        data - The top level dictionary of the pyproject.toml file
                    If not provided, a pyproject.toml will be discovered and loaded directly
        """

        self.enabled = False

        def extract_plugin(namespace_package, plugin_type) -> list:
            """
            Import all plugins from a namespace
            """

            plugin_types = []

            for _, name, is_package in pkgutil.iter_modules(
                namespace_package.__path__, namespace_package.__name__ + "."
            ):
                if not is_package:
                    module = importlib.import_module(name)
                    class_members = inspect.getmembers(module, inspect.isclass)
                    for (_, value) in class_members:
                        if issubclass(value, plugin_type) & (value is not plugin_type):
                            if value.valid():
                                plugin_types.append(value)

            return plugin_types

        # Load the interface plugin
        interface_type = extract_plugin(cppython.plugins.interface, Interface)

        # Load the generator plugin
        generator_type = extract_plugin(cppython.plugins.generator, Generator)

        # Plugin error checking
        if interface_type is None:
            return

        if generator_type is None:
            return

        if len(interface_type) > 1:
            return

        if len(generator_type) > 1:
            return

        interface_type = interface_type.pop()
        generator_type = generator_type.pop()

        # No-op construction ends here.
        self.enabled = True

        # Construct and extract the interface data
        self._interface = interface_type()
        data = self._interface.read_pyproject()
        info = self._interface.pep_612()

        # Extract and construct the generator data
        metadata = generator_type.extract_metadata(data)
        self._generator = generator_type(info, metadata)

    def install(self) -> None:
        self._generator.install()

    def update(self) -> None:
        self._generator.update()

    def build(self) -> None:
        self._generator.build()

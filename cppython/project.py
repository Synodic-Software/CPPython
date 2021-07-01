from pathlib import Path

from cppython.schema import API, Interface, Generator

import cppython.plugins.generator
import cppython.plugins.interface

import pkgutil
import importlib
import inspect


class Project(API):
    def __init__(self, path: Path, interface_type: Interface = None, data: dict = {}) -> None:
        """
        data - The top level dictionary of the pyproject.toml file
                    If not provided, a pyproject.toml will be discovered and loaded directly
        """

        self.enabled = False
        self.dirty = False

        # TODO: Data writing
        if not data:
            data = self._find_pyproject(path)

        def extract_plugin(namespace_package, plugin_type):
            """
            Import all plugins from a namespace
            """

            for _, name, is_package in pkgutil.iter_modules(
                namespace_package.__path__, namespace_package.__name__ + "."
            ):
                if not is_package:
                    module = importlib.import_module(name)
                    class_members = inspect.getmembers(module, inspect.isclass)
                    for (_, value) in class_members:
                        if issubclass(value, plugin_type) & (value is not plugin_type):
                            if value.valid(data):
                                return value
            return None

        # Load the interface plugin if it is not defined by the entrypoint
        if interface_type is None:
            interface_type = extract_plugin(cppython.plugins.interface, Interface)

        # Load the generator plugin
        generator_type = extract_plugin(cppython.plugins.generator, Generator)

        # Check validity
        if interface_type is None or generator_type is None:
            return

        # No-op construction ends here.
        self.enabled = True

        # Construct and extract the interface data
        self._interface = interface_type()
        info = self._interface.gather_pep_612(data)

        # Extract and construct the generator data
        metadata = generator_type.extract_metadata(data)
        self._generator = generator_type(info, metadata)

    def _find_pyproject(self, path: Path) -> dict:
        """
        Finds and reads the first pyproject.toml file starting with the given directory, travelling upward.
        """

        if path.is_file():
            path = path.parent

        while not path.glob("pyproject.toml"):
            if path.is_absolute():
                assert "This is not a valid project. No pyproject.toml found in the current directory or any of its parents."

        import tomlkit

        return tomlkit.loads(Path(path / "pyproject.toml").read_text(encoding="utf-8"))

    def install(self) -> None:
        self._generator.install()

    def update(self) -> None:
        self._generator.update()

from pathlib import Path

from cppython.schema import API, Interface


class Project(API):
    def __init__(self, path: Path, interface_type: Interface = None, data: dict = {}) -> None:
        """
        data - The top level dictionary of the pyproject.toml file
                    If not provided, pyproject.toml will be loaded directly
        """

        self.enabled = False
        self.dirty = False

        # TODO: If data is loaded directly it needs to be written out
        if not data:

            if path.is_file():
                path = path.parent

            while not path.glob("pyproject.toml"):
                if path.is_absolute():
                    assert "This is not a valid project. No pyproject.toml found in the current directory or any of its parents."

            # TODO: Use tomlkit
            import toml

            data = toml.load(path / "pyproject.toml")

        # Prepare for plugin loading
        import pkgutil
        import importlib
        import inspect

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

            import cppython.plugins.interface

            interface_type = extract_plugin(cppython.plugins.interface, Interface)

        # This is not a valid project.
        if interface_type is None:
            return

        # Load the generator plugin
        import cppython.plugins.generator

        from cppython.schema import Generator

        generator_type = extract_plugin(cppython.plugins.generator, Generator)

        # This is not a valid project.
        if interface_type is None or generator_type is None:
            return

        # Pass-through initialization ends here
        self.enabled = True

        # Construct and extract the interface data
        self._interface = interface_type()
        info = self._interface.gather_pep_612(data)

        # Extract and construct the generator data
        metadata = generator_type.extract_metadata(data)
        self._generator = generator_type(info, metadata)

    def install(self) -> None:
        self._generator.install()

    def update(self) -> None:
        self._generator.update()
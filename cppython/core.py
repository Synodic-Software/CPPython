from pathlib import Path
from cerberus import Validator
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

import importlib
import pkgutil
import inspect

# TODO: Comment
import cppython.plugins


@dataclass(frozen=True)
class PEP621:
    """
    Subset of PEP 621
        The entirety of PEP 621 is not relevant for this plugin
        Link: https://www.python.org/dev/peps/pep-0621/
    """

    name: str
    version: str
    description: str
    readme: str
    requires_python: str
    license: str
    authors: str
    maintainers: str
    keywords: str
    classifiers: str
    urls: str

    def __post_init__(self):
        """
        Manual validation per attribute
            TODO: Remove with Cerberus 2.0
        """

        # TODO: Unify with dataclass definition with Cerberus 2.0
        schema = {
            "name": {"type": "string"},  # TODO: Normalize for internal consumption - PEP 503
            "version": {"type": "string"},  # TODO:  Make Version type
            "description": {"type": "string"},
            "readme": {"type": "string"},  # TODO: String or table
            "requires_python": {"type": "string"},  # TODO: Version type
            "license": {"type": "string"},  # TODO: Table specification
            "authors": {"type": "string"},  # TODO:  specification
            "maintainers": {"type": "string"},  # TODO:  specification
            "keywords": {"type": "string"},  # TODO:  specification
            "classifiers": {"type": "string"},  # TODO:  specification
            "urls": {"type": "string"},  # TODO:  specification
        }

        _validator = Validator(schema)

        if not _validator.validate(asdict(self)):
            msg = f"'{type(self).__name__}' validation failed: {_validator.errors}"
            raise AttributeError(msg)


@dataclass
class Metadata:
    """
    TODO: Description
    """

    # TODO: Unify with dataclass definition with Cerberus 2.0
    _schema = {
        "remotes": {
            "type": "list",
            "empty": True,
            "schema": {"type": "list", "items": [{"type": "string"}, {"type": "string"}]},  # TODO: Make URL type
        },
        "dependencies": {
            "type": "dict",
            "keysrules": {"type": "string"},  # TODO Proper PyPi names?
            "valuesrules": {"type": "string"},  # TODO:  Make Version type
        },
        "install_path": {"type": "string"},  # TODO: Make Path type
    }

    _validator = Validator()

    remotes: str
    dependencies: str
    install_path: str

    def __getattribute__(self, name):
        """
        Lazily validate attributes as they are accessed
        """
        if not self._validator.validate(object.__getattribute__(self, name), schema=self._schema[name]):
            msg = f"'{type(self).__name__}' validation failed: {self._validator.errors}"
            raise AttributeError(msg)

    def validate(self):
        """
        Validate all attributes
        """
        if not self._validator.validate(asdict(self), schema=self._schema):
            msg = f"'{type(self).__name__}' validation failed: {self._validator.errors}"
            raise AttributeError(msg)


class Plugin(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def valid(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def gather_pep_612(self, data: dict) -> PEP621:
        raise NotImplementedError()


class Project:
    def __init__(self, path: Path, data: dict = {}) -> None:
        """
        data - The top level dictionary of the pyproject.toml file
                    If not provided, pyproject.toml will be loaded internally
        """

        self.enabled = False
        self.dirty = False

        # TODO: If data is loaded, it needs to be written out as well
        if not data:

            if path.is_file():
                path = path.parent

            while not path.glob("pyproject.toml"):
                if path.is_absolute():
                    assert "This is not a valid project. No pyproject.toml found in the current directory or any of its parents."

            import tomlkit

            pyproject = path / "pyproject.toml"
            data = dict(tomlkit.parse(pyproject.read_text("utf-8")))

        # Deactivate this plugin based on the presence of the 'conan' table
        if "tool" not in data or "conan" not in data["tool"]:
            return

        # import all plugins from the namespace

        def extract_plugin(namespace_package):
            for _, name, is_package in pkgutil.iter_modules(
                namespace_package.__path__, namespace_package.__name__ + "."
            ):
                if not is_package:
                    module = importlib.import_module(name)
                    class_members = inspect.getmembers(module, inspect.isclass)
                    for (_, value) in class_members:
                        if issubclass(value, Plugin) & (value is not Plugin):
                            plugin = value()
                            if plugin.valid():
                                return plugin
            return None

        project_plugin = extract_plugin(cppython.plugins)

        # This is not a valid project.
        if project_plugin is None:
            return

        # Pass-through initialization ends here
        self.enabled = True

        # Maintain the input data for writing capabilities
        self._data = data["tool"]["conan"]

        def normalize(data: dict) -> dict:
            """
            Returns a copy of the original with key names normalized
            """

            return {key.replace("-", "_"): value for (key, value) in data.items()}

        self.info = project_plugin.gather_pep_612(data)

        # The dataclass 'Metadata' may contain improper attributes.
        try:
            self.metadata = Metadata(**normalize(self._data))
        except TypeError:
            Metadata.validate(self._data)

    def validate(self):
        self.metadata.validate()


class _BaseGenerator:
    def __init__(self, project: Project) -> None:
        self._project = project


class ConanGenerator(_BaseGenerator):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def write_file(self, path: Path) -> None:
        #     Generate a conanfile.py with the given path.
        #     The resulting recipe is TODO
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "conanfile.py", "w+") as file:

            # Process the Conan data into a Conan format
            name = self._project["name"]
            name = name.replace("-", "")

            dependencies = ["/".join(tup) for tup in self._project["dependencies"].items()]
            dependencies = ",".join(f'"{dep}"' for dep in dependencies)

            # Write the Conan data to file
            # TODO: Require the conan version that this plugin depends on
            contents = (
                f"from conans import ConanFile, CMake\n"
                f"\n"
                f"required_conan_version = '>=1.37.1'\n"
                f"\n"
                f"class {name}Conan(ConanFile):\n"
                f"    settings = 'os', 'compiler', 'build_type', 'arch'\n"
                f"    requires = {dependencies}\n"
                f"    generators = ['cmake_find_package', 'cmake_paths']\n"
            )

            print(contents, file=file)

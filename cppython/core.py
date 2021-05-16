from pathlib import Path
from cerberus import Validator
from collections.abc import MutableMapping
from abc import ABC, abstractmethod
from importlib.metadata import entry_points

import importlib
import pkgutil
import cppython.plugins

class Plugin(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def valid(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def gather_pep_612(self, data: dict) -> dict:
        raise NotImplementedError()


class Project(MutableMapping):

    """
    Schema for subset of PEP 621
        The entirety of PEP 621 is not relevant for this plugin
        Link: https://www.python.org/dev/peps/pep-0621/
    """

    _project_schema = {
        "name": {"type": "string"},  # TODO: Normalize for internal consumption - PEP 503
        "version": {"type": "string"},  # TODO:  Make Version type
        "description": {"type": "string"},
        "readme": {"type": "string"},  # TODO: String or table
        "requires-python": {"type": "string"},  # TODO: Version type
        "license": {"type": "string"},  # TODO: Table specification
        "authors": {"type": "string"},  # TODO:  specification
        "maintainers": {"type": "string"},  # TODO:  specification
        "keywords": {"type": "string"},  # TODO:  specification
        "classifiers": {"type": "string"},  # TODO:  specification
        "urls": {"type": "string"},  # TODO:  specification
    }

    _conan_schema = {
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
        "install-path": {"type": "string"},  # TODO: Make Path type
    }

    def __init__(self, path: Path, data: dict = {}) -> None:

        if not data:

            if path.is_file():
                path = path.parent

            while not path.glob("pyproject.toml"):
                if path.is_absolute():
                    assert "This is not a valid project."

            import toml

            data = toml.load(path / "pyproject.toml")

        # import all plugins from the internal namespace

            def iter_namespace(ns_pkg):
                # Specifying the second argument (prefix) to iter_modules makes the
                # returned name an absolute name instead of a relative one. This allows
                # import_module to work without having to do additional modification to
                # the name.
                return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

        internal_plugins = {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in iter_namespace(cppython.plugins)
        }

        # import all plugins from the external environment
        external_plugins = entry_points(group='cppython.plugins')

        plugins = []

        project_plugin = None
        
        for plugin in plugins:
            if plugin.valid():
                project_plugin = plugin

        if project_plugin is None:
            assert "This is not a valid project."

        self._data = project_plugin.gather_pep_612(data)

        self._project_validator = Validator(schema=Project._project_schema)
        self._conan_validator = Validator(schema=Project._conan_schema)

        self._metadata = data["tool"]["conan"]

        self.dirty = False

    def __setitem__(self, key, value):
        self.dirty = True
        self._metadata[self._keytransform(key)] = value

    def __getitem__(self, key):
        key = self._keytransform(key)

        if self._conan_validator.validate(self._metadata, {key: Project._conan_schema[key]}):
            return self._metadata[key]

        msg = f"'{type(self).__name__}' failed validation with attribute '{key}'. Errors: {self._conan_validator.errors}"
        raise AttributeError(msg)

    def __delitem__(self, key):
        del self._metadata[self._keytransform(key)]

    def __iter__(self):
        return iter(self._metadata)

    def __len__(self):
        return len(self._metadata)

    def _keytransform(self, key):
        return key

    def _validate_project_key(self, key):
        if self._project_validator.validate(self._data, {key: Project._project_schema[key]}):
            return self._data[key]

        msg = f"'{type(self).__name__}' failed validation with attribute '{key}'. Errors: {self._project_validator.errors}"
        raise AttributeError(msg)

    @property
    def name(self) -> str:
        return self._validate_project_key("name")

    @property
    def version(self) -> str:
        return self._validate_project_key("version")

    @property
    def description(self) -> str:
        return self._validate_project_key("description")

    @property
    def readme(self) -> str:
        return self._validate_project_key("readme")

    @property
    def requires_python(self) -> str:
        return self._validate_project_key("requires-python")

    @property
    def license(self) -> str:
        return self._validate_project_key("license")

    @property
    def authors(self) -> str:
        return self._validate_project_key("authors")

    @property
    def maintainers(self) -> str:
        return self._validate_project_key("maintainers")

    @property
    def keywords(self) -> str:
        return self._validate_project_key("keywords")

    @property
    def classifiers(self) -> str:
        return self._validate_project_key("classifiers")

    @property
    def urls(self) -> str:
        return self._validate_project_key("urls")

    def validate(self):
        if not self._project_validator.validate(self, self._project_schema):
            msg = f"Failed project validation with {self._project_validator.errors}"
            raise AttributeError(msg)

        if not self._conan_validator.validate(self, self._conan_schema):
            msg = f"Failed conan validation with {self._conan_validator.errors}"
            raise AttributeError(msg)


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
                f"required_conan_version = '>=1.36.0'\n"
                f"\n"
                f"class {name}Conan(ConanFile):\n"
                f"    settings = 'os', 'compiler', 'build_type', 'arch'\n"
                f"    requires = {dependencies}\n"
                f"    generators = ['cmake_find_package', 'cmake_paths']\n"
            )

            print(contents, file=file)

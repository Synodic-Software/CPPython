from pathlib import Path
from cerberus import Validator
from collections.abc import MutableMapping


class Project:

    """
    Schema for subset of PEP 621
        The entirety of PEP 621 is not relevant for this plugin
        Link: https://www.python.org/dev/peps/pep-0621/
    """

    _schema = {
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

    def __init__(self, data: dict) -> None:

        self._validator = Validator(schema=Project._schema, allow_unknown=True)
        self._data = data


class Metadata(MutableMapping):

    _schema = {
        "remotes": {
            "type": "list",
            "empty": True,
            "schema": {"type": "list", "items": [{"type": "string"}, {"type": "string"}]},  # TODO: Make URL type
        },
        "dependencies": {
            "type": "dict",
            "schema": {
                "type": "list",
                "items": [{"type": "string"}, {"type": "string"}],  # TODO: Make Version type
            },
        },
        "install-path": {"type": "string"},  # TODO: Make Path type
    }

    def __init__(self, *args, **kwargs) -> None:
        self.update(dict(*args, **kwargs))

        self._validator = Validator(schema=Metadata._schema, allow_unknown=True)

        self.dirty = False

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    # def __getattr__(self, name):

    #     if name in Metadata._schema:
    #         if self._validator.validate(self._data, {name: Metadata._schema[name]}):
    #             return self._data[name]

    #         msg = f"'{type(self).__name__}' failed validation with attribute '{name}'. Errors: {self._validator.errors}"
    #         raise AttributeError(msg)

    #     msg = f"'{type(self).__name__}' object has no attribute '{name}'"
    #     raise AttributeError(msg)

    # def __setattr__(self, name, value):
    #     if name in self._frozen_variables:
    #         super().__setattr__(name, value)

    #     else:
    #         if name in self._data:
    #             self.dirty = True
    #             self._data[name] = value
    #         else:
    #             msg = f"'{type(self).__name__}' object has no attribute '{name}'"
    # raise AttributeError(msg)

    def validate(self) -> None:

        if not self._validator.validate(self, self._schema):
            msg = f"Failed validation with {self._validator.errors}"
            raise AttributeError(msg)


class _BaseGenerator:
    def __init__(self, metadata: Metadata) -> None:
        self._metadata = metadata


class ConanGenerator(_BaseGenerator):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def write_file(self, path: Path) -> None:
        #     Generate a conanfile.py with the given path.
        #     The resulting recipe is TODO
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "conanfile.py", "w+") as file:

            # Process the Conan data into a Conan format
            name = self._metadata.name
            name = name.replace("-", "")

            dependencies = ["/".join(tup) for tup in self._metadata.dependencies.items()]
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

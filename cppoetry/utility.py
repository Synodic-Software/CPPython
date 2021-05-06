from tomlkit.toml_document import TOMLDocument
from tomlkit.exceptions import NonExistentKey

from pathlib import Path
from typing import Callable


class _BaseGenerator:
    def __init__(self, metadata: "MetaData") -> None:
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
                f'required_conan_version = ">=1.36.0"\n'
                f"\n"
                f"class {name}Conan(ConanFile):\n"
                f'    settings = "os", "compiler", "build_type", "arch"\n'
                f"    requires = {dependencies}\n"
                f'    generators = ["cmake_find_package", "cmake_paths"]\n'
            )

            print(contents, file=file)


class Metadata:

    # Schema for poetry values
    _poetry_schema = {
        "name": {"type": "string"},
        "version": {"type": "string"},  # TODO: Make Version type
    }

    # Schema for Conan values
    _conan_schema = {
        "remotes": {"type": "list", "schema": {"type": "tuple", "items": ({"type": "string"}, {"type": "string"})}},
        "dependencies": {
            "type": "list",
            "schema": {
                "type": "tuple",
                "items": ({"type": "string"}, {"type": "string"}),  # TODO: Make Version type
            },
        },
        "install_directory": {"type": "string"},  # TODO: Make Path type
    }

    _frozen_variables = {
        "_root",
        "_validator",
        "_generator",
        "_poetry_data",
        "_conan_data",
        "dirty",
    }

    def __init__(self, root: Path, document: TOMLDocument) -> None:

        from cerberus import Validator

        self._root = root.absolute()  # TODO: Only required for Generator
        self._validator = Validator()
        self._generator = ConanGenerator(document)  # TODO: Make external to Metadata

        # Gather data from the document
        # TODO: Error handling for these document tabs
        self._poetry_data = document["tool"]["poetry"]
        self._conan_data = document["tool"]["conan"]

        self.dirty = False

    def __getattr__(self, name):

        if name in Metadata._poetry_schema:
            if not self._validator.validate(self._poetry_data, Metadata._poetry_schema[name]):
                return self._poetry_data[name]

            msg = f"'{type(self).__name__}' failed Poetry validation with attribute '{name}'"
            raise AttributeError(msg)

        if name in Metadata._conan_schema:
            if not self._validator.validate(self._conan_data, Metadata._conan_schema[name]):
                return self._conan_data[name]

            msg = f"'{type(self).__name__}' failed Conan validation with attribute '{name}'"
            raise AttributeError(msg)

        msg = f"'{type(self).__name__}' object has no attribute '{name}'"
        raise AttributeError(msg)

    def __setattr__(self, name, value):
        if name in self._frozen_variables:
            super().__setattr__(name, value)

        else:
            if name in self._poetry_data:
                self.dirty = True
                self._poetry_data[name] = value
            elif name in self._conan_data:
                self.dirty = True
                self._conan_data[name] = value
            else:
                msg = f"'{type(self).__name__}' object has no attribute '{name}'"
                raise AttributeError(msg)

    def generate_conanfile(self) -> None:
        self._generator.write_file(self._root)

    def validate(self) -> None:
        if self._validator.validate(self._poetry_data, self._poetry_schema) or self._validator.validate(
            self._conan_data, self._conan_schema
        ):
            msg = f"Failed Validation"
            raise AttributeError(msg)

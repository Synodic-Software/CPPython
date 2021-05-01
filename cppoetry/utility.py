from tomlkit.toml_document import TOMLDocument
from tomlkit.exceptions import NonExistentKey

from cerberus import Validator

from pathlib import Path


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
    def __init__(self, root: Path, document: TOMLDocument) -> None:

        self._root = root.absolute()
        self._document = document
        self._validator = Validator()
        self._generator = ConanGenerator()

        self.dirty = False

    def __getattr__(self, name):
        try:
            return self.__dict[name]
        except KeyError:
            msg = "'{0}' object has no attribute '{1}'"
            raise AttributeError(msg.format(type(self).__name__, name))

    def __setattr__(self, name, value):
        if name in self.data:
            self.data[name] = value
        else:
            super().__setattr__(name, value)

    def generate_conanfile(self) -> None:
        self._generator.write_file(self._root)

    @property
    def name(self) -> str:
        try:
            self._name = self.document["tool"]["poetry"]["name"]

        except NonExistentKey:
            try:
                self._name = self.document["tool"]["poetry"]["name"]
            except NonExistentKey:
                raise LookupError("The project's TOML file does not contain a name")

        return self._name

    @name.setter
    def name(self, value: str) -> None:

        self.dirty = True
        self._name = value

    @property
    def remotes(self) -> list[tuple[str, str]]:
        try:
            self._remotes = self.document["tool"]["conan"]["remotes"]

        except NonExistentKey:
            raise LookupError("The project's TOML file does not contain a remotes value")

        return self._remotes

    @remotes.setter
    def remotes(self, values: list[tuple[str, str]]) -> None:

        self.dirty = True
        self._remotes = values

    @property
    def dependencies(self) -> dict[str]:
        try:
            self._dependencies = self.document["tool"]["conan"]["dependencies"]

        except NonExistentKey:
            raise LookupError("The project's TOML file does not contain dependencies")

        return self._dependencies

    @dependencies.setter
    def dependencies(self, values: dict[str]) -> None:

        self.dirty = True
        self._dependencies = values

    @property
    def install_directory(self) -> Path:
        try:
            self._install_directory = Path(self.document["tool"]["conan"]["install-directory"])

        except NonExistentKey:
            self._install_directory = Path("build")

        if not self._install_directory.is_absolute():
            self._install_directory = self.root / self._install_directory

        return self._install_directory

    @install_directory.setter
    def install_directory(self, value: Path) -> None:

        self.dirty = True
        self._install_directory = value

    @property
    def version(self) -> Path:
        try:
            self._version = self.document["tool"]["poetry"]["version"]

        except NonExistentKey:
            raise LookupError("The project's TOML file does not contain a version")

        return self._version

    @version.setter
    def version(self, value: str) -> None:

        self.dirty = True
        self._version = value

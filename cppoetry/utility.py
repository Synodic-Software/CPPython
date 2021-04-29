from tomlkit.toml_document import TOMLDocument
from tomlkit.exceptions import NonExistentKey

from pathlib import Path


class Metadata:
    def __init__(self, document: TOMLDocument) -> None:

        self.document = document
        self.dirty = False

    def generate_conanfile(self) -> Path:

#     Generate a conanfile.py with the given path.
#     The resulting recipe is TODO
#     """
#     path = path.absolute()
#     path.mkdir(parents=True, exist_ok=True)
#     with open(path / "conanfile.py", "w+") as file:

#         # Process the Conan data into a Conan format
#         name = SynodicPlugin.data["tool"]["poetry"]["name"]
#         name = name.replace("-", "")

#         dependencies = ["/".join(tup) for tup in SynodicPlugin.data["tool"]["conan"]["dependencies"].items()]
#         dependencies = ",".join('"{0}"'.format(w) for w in dependencies)

#         generators = ",".join('"{0}"'.format(g) for g in SynodicPlugin.generators)

#         # Write the Conan data to file
#         contents = (
#             f"from conans import ConanFile, CMake\n"
#             f"\n"
#             f"class {name}Conan(ConanFile):\n"
#             f'    settings = "os", "compiler", "build_type", "arch"\n'
#             f"    requires = {dependencies}\n"
#             f"    generators = {generators}\n"
#         )

#         print(contents, file=file)


        return Path()

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
    def remotes(self) -> list[str]:
        try:
            self._remotes = self.document["tool"]["conan"]["remotes"]

        except NonExistentKey:
            raise LookupError("The project's TOML file does not contain a name")

        return self._remotes

    @remotes.setter
    def remotes(self, values: list[str]) -> None:

        self.dirty = True
        self._remotes = values

    @property
    def dependencies(self) -> list[str]:
        try:
            self._remotes = self.document["tool"]["conan"]["dependencies"]

        except NonExistentKey:
            raise LookupError("The project's TOML file does not contain a name")

        return self._remotes

    @dependencies.setter
    def dependencies(self, values: list[str]) -> None:

        self.dirty = True
        self._remotes = values
        
        

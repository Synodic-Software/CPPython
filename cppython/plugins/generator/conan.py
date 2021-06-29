from cppython.schema import Generator, Metadata
from conans.client.conan_api import ConanAPIV1 as ConanAPI
from cppython.core import Project, ConanGenerator

from pathlib import Path


class ConanMetadata(Metadata):
    """
    Additional metadata required by Conan generator
    """

    generator: str # TODO: Give a proper type

class ConanGenerator(Generator):
    """
    Conan generator plugin
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def write_file(self, path: Path) -> None:
        #     Generate a conanfile.py with the given path.
        #     The resulting recipe is TODO
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "conanfile.py", "w+") as file:

            # Process the Conan data into a Conan format
            name = self._project.info.name
            name = name.replace("-", "")

            dependencies = ["/".join(tup) for tup in self._project.metadata.dependencies.items()]
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



class CPPythonAPI:
    def __init__(self, root: Path, project: Project):
        self._root = root.absolute()
        self._project = project
        self._generator = ConanGenerator(self._project)

    def install(self):
        self._generator.write_file(self._root)

        for remote_name, url in self._project.metadata.remotes:
             ConanAPI().remote_add(remote_name, url)

        ConanAPI().install(
            path=str(self._root),
            name=self._project.info.name,
            version=self._project.info.version,
            user=None,
            channel=None,
            settings=None,
            options=None,
            env=["CONAN_USER_HOME=.conan-cache"],
            remote_name=None,  # Let the selection happen automatically from the 'conan remote' command
            verify=None,
            manifests=None,
            manifests_interactive=None,
            build=None,
            profile_names=None,
            update=False,
            generators=None,
            no_imports=False,
            install_folder=str(self._project.metadata.installation),
            cwd=str(self._project.metadata.installation),
            lockfile=None,
            lockfile_out=None,
            profile_build=None,
        )

    def update(self):
        self._generator.write_file(self._root)

        for remote_name, url in self._project.metadata.remotes:
             ConanAPI().remote_add(remote_name, url)

        ConanAPI().install(
            path=str(self._root),
            name=self._project.info.name,
            version=self._project.info.version,
            user=None,
            channel=None,
            settings=None,
            options=None,
            env=["CONAN_USER_HOME=.conan-cache"],
            remote_name=None,  # Let the selection happen automatically from the 'conan remote' command
            verify=None,
            manifests=None,
            manifests_interactive=None,
            build=None,
            profile_names=None,
            update=True,
            generators=None,
            no_imports=False,
            install_folder=str(self._project.metadata.installation),
            cwd=str(self._project.metadata.installation),
            lockfile=None,
            lockfile_out=None,
            profile_build=None,
        )

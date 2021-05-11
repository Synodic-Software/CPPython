from conans.client.conan_api import ConanAPIV1 as ConanAPI
from cppython.data import Metadata, ConanGenerator

from pathlib import Path


class CPPythonAPI:
    def __init__(self, root: Path, metadata: Metadata):
        self._root = root.absolute()
        self._metadata = metadata
        self._generator = ConanGenerator(self._metadata)

    def install(self):
        self._generator.write_file(self._root)

        for remote_name, url in self._metadata.remotes:
             ConanAPI().remote_add(remote_name, url)

        ConanAPI().install(
            path=str(self._root),
            name=self._metadata.name,
            version=self._metadata.version,
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
            install_folder=str(self._metadata.install_directory),
            cwd=str(self._metadata.install_directory),
            lockfile=None,
            lockfile_out=None,
            profile_build=None,
        )

    def update(self):
        self._generator.write_file(self._root)

        for remote_name, url in self._metadata.remotes:
             ConanAPI().remote_add(remote_name, url)

        ConanAPI().install(
            path=str(self._root),
            name=self._metadata.name,
            version=self._metadata.version,
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
            install_folder=str(self._metadata.install_directory),
            cwd=str(self._metadata.install_directory),
            lockfile=None,
            lockfile_out=None,
            profile_build=None,
        )

    def validate(self):
        self._metadata.validate()

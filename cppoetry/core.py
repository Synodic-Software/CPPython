from conans.client.conan_api import ConanAPIV1 as ConanAPI
from cppoetry.utility import Metadata

from pathlib import Path


class CPPoetryAPI:
    def __init__(self, root: Path, metadata: Metadata):
        self.root = root.absolute()
        self.metadata = metadata

    def install(self):
        self.metadata.generate_conanfile()

        for remote_name, url in self.metadata.remotes:
             ConanAPI().remote_add(remote_name, url)

        ConanAPI().install(
            path=str(self.root),
            name=self.metadata.name,
            version=self.metadata.version,
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
            install_folder=str(self.metadata.install_directory),
            cwd=str(self.metadata.install_directory),
            lockfile=None,
            lockfile_out=None,
            profile_build=None,
        )

    def update(self):
        self.metadata.generate_conanfile()

        for remote_name, url in self.metadata.remotes:
             ConanAPI().remote_add(remote_name, url)

        ConanAPI().install(
            path=str(self.root),
            name=self.metadata.name,
            version=self.metadata.version,
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
            install_folder=str(self.metadata.install_directory),
            cwd=str(self.metadata.install_directory),
            lockfile=None,
            lockfile_out=None,
            profile_build=None,
        )

    def validate(self):
        self.metadata.validate()

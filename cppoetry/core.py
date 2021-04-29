from conans.client.conan_api import ConanAPIV1 as ConanAPI
from cppoetry.utility import Metadata

from pathlib import Path


class CPPoetryAPI:
    def __init__(self, metadata: Metadata):
        self.metadata = metadata

    def install(self):
        self.metadata.generate_conanfile()

        ConanAPI().install(
            path=str(Path().absolute()),
            name=self.metadata.name,
            version=self.metadata.version,
            user=None,
            channel=None,
            settings=None,
            options=None,
            env=None,
            remote_name=None,
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

        ConanAPI().install(
            path=str(Path().absolute()),
            name=self.metadata.name,
            version=self.metadata.version,
            user=None,
            channel=None,
            settings=None,
            options=None,
            env=None,
            remote_name=self.metadata.remotes,
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
        properties = [name for name, value in vars(Metadata).items() if isinstance(value, property)]

        for prop in properties:
            print(getattr(self.metadata, prop))

from conans.client.conan_api import ConanAPIV1 as ConanAPI
from cppoetry.utility import Metadata

from pathlib import Path

class CPPoetryAPI:
    def __init__(self, Metadata):
        pass

    def install(self):
        ConanAPI().install(
            path=None,  # SynodicPlugin.data["tool"]["conan"]["install-path"],
            name=None,  # SynodicPlugin.data["tool"]["poetry"]["name"],
            version=None,  # SynodicPlugin.data["tool"]["poetry"]["version"],
            user=None,
            channel=None,
            settings=None,
            options=None,
            env=None,
            remote_name=None,  # SynodicPlugin.data["tool"]["conan"]["remotes"],
            verify=None,
            manifests=None,
            manifests_interactive=None,
            build=None,
            profile_names=None,
            update=False,
            generators=None,
            no_imports=False,
            install_folder=None,  # SynodicPlugin.data["tool"]["conan"]["install-path"],
            cwd=Path().absolute(),
            lockfile=None,
            lockfile_out=None,
            profile_build=None,
        )

    def update(self):
        ConanAPI().install(
            path=None,  # SynodicPlugin.data["tool"]["conan"]["install-path"],
            name=None,  # SynodicPlugin.data["tool"]["poetry"]["name"],
            version=None,  # SynodicPlugin.data["tool"]["poetry"]["version"],
            user=None,
            channel=None,
            settings=None,
            options=None,
            env=None,
            remote_name=None,  # SynodicPlugin.data["tool"]["conan"]["remotes"],
            verify=None,
            manifests=None,
            manifests_interactive=None,
            build=None,
            profile_names=None,
            update=True,
            generators=None,
            no_imports=False,
            install_folder=None,  # SynodicPlugin.data["tool"]["conan"]["install-path"],
            cwd=Path().absolute(),
            lockfile=None,
            lockfile_out=None,
            profile_build=None,
        )

    def validate(self):
        pass
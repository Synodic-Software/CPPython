from conans.client.conan_api import ConanAPIV1 as ConanAPI

from pathlib import Path

class CPPoetryAPI:

    def __init__(self):
        pass

    def new(self):
        pass


    def init(self):
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
        )


    def add(self):
        pass


    def remove(self):
        pass


    def show(self):
        pass


    def build(self):
        pass


    def publish(self):
        pass


    def config(self):
        pass


    def run(self):
        pass


    def shell(self):
        pass


    def check(self):
        pass


    def search(self):
        pass


    def lock(self):
        pass


    def version(self):
        pass


    def export(self):
        pass


    def env(self):
        pass


    def cache(self):
        pass
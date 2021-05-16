from conans.client.conan_api import ConanAPIV1 as ConanAPI
from cppython.data import Project, ConanGenerator

from pathlib import Path


class CPPythonAPI:
    def __init__(self, root: Path, project: Project):
        self._root = root.absolute()
        self._project = project
        self._generator = ConanGenerator(self._project)

    def install(self):
        self._generator.write_file(self._root)

        for remote_name, url in self._project['remotes']:
             ConanAPI().remote_add(remote_name, url)

        ConanAPI().install(
            path=str(self._root),
            name=self._project.name,
            version=self._project.version,
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
            install_folder=str(self._project['install_directory']),
            cwd=str(self._project['install_directory']),
            lockfile=None,
            lockfile_out=None,
            profile_build=None,
        )

    def update(self):
        self._generator.write_file(self._root)

        for remote_name, url in self._project['remotes']:
             ConanAPI().remote_add(remote_name, url)

        ConanAPI().install(
            path=str(self._root),
            name=self._project.name,
            version=self._project.version,
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
            install_folder=str(self._project['install_directory']),
            cwd=str(self._project['install_directory']),
            lockfile=None,
            lockfile_out=None,
            profile_build=None,
        )

    def validate(self):
        self._project.validate()

import toml

from pathlib import Path as _Path
from conans.client.conan_api import ConanAPIV1 as _ConanAPI


class SynodicPlugin:

    data = None

    def __init_data(self):
        """
        TODO: Remove hardcoded extraction once poetry has plugin support
        """

        if not self.data:
            pyProject = _Path("pyproject.toml")
            self.data = toml.load(pyProject)

            poetryData = self.data["tool"]["poetry"]
            conanData = self.data["tool"]["conan"]

            self.name = poetryData["name"]
            self.version = poetryData["version"]

            self.installPath = _Path(conanData["install-path"]).absolute()
            self.remotes = conanData["remotes"]

            # Dependencies require some post processing
            self.dependencies = conanData["dependencies"]

            # Dependencies require some post processing
            self.generators = conanData["generators"]
            assert len(self.generators) > 0

            # Generate the conanfile.txt
            # TODO: remove once conan can depend on pyproject.toml
            self.installPath.mkdir(parents=True, exist_ok=True)
            with open(self.installPath / "conanfile.txt", "w+") as file:
                file.write("[requires]")
                for key, value in self.dependencies.items():
                    file.write(key + "/" + value)

                file.write("\n[generators]")
                for generator in self.generators:
                    file.write(generator)

    def poetry_new(self):

        pass

    def poetry_init(self):

        pass

    def poetry_install(self):

        self.__init_data()

        _ConanAPI().install(
            path=self.installPath,
            name=self.name,
            version=self.version,
            user=None,
            channel=None,
            settings=None,
            options=None,
            env=None,
            remote_name=self.remotes,
            verify=None,
            manifests=None,
            manifests_interactive=None,
            build=None,
            profile_names=None,
            update=False,
            generators=None,
            no_imports=False,
            install_folder=self.installPath,
            cwd=_Path().absolute(),
            lockfile=None,
        )

    def poetry_update(self):

        self.__init_data()

        _ConanAPI().install(
            path=self.installPath,
            name=self.name,
            version=self.version,
            user=None,
            channel=None,
            settings=None,
            options=None,
            env=None,
            remote_name=self.remotes,
            verify=None,
            manifests=None,
            manifests_interactive=None,
            build=None,
            profile_names=None,
            update=True,
            generators=None,
            no_imports=False,
            install_folder=self.installPath,
            cwd=_Path().absolute(),
            lockfile=None,
        )

    def poetry_add(self):

        pass

    def poetry_remove(self):

        pass

    def poetry_show(self):

        pass

    def poetry_build(self):

        pass

    def poetry_publish(self):

        pass

    def poetry_config(self):

        pass

    def poetry_check(self):

        pass

    def poetry_search(self):

        pass

    def poetry_lock(self):

        pass

    def poetry_version(self):

        pass

    def poetry_export(self):

        pass

    def poetry_env(self):

        pass

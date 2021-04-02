from tomlkit import parse

from cleo.io.io import IO as _IO

from poetry.plugins.plugin import Plugin as _Plugin
from poetry.poetry import Poetry as _Poetry

from pathlib import Path as _Path
from conans.client.conan_api import ConanAPIV1 as _ConanAPI


class SynodicPlugin(_Plugin):

    data = None
    generators = ["cmake_find_package", "cmake_paths"]

    def __init__(self):
        """
        TODO: Remove hardcoded extraction once poetry has plugin support
        """

        if not SynodicPlugin.data:
            with open("pyproject.toml", "r") as file:
                SynodicPlugin.data = parse(file.read())

            # Generate the conanfile.py
            self.__write_conanfile(
                _Path(SynodicPlugin.data["tool"]["conan"]["install-path"])
            )

    def __write_conanfile(self, path: _Path):
        """
        Generate a conanfile.py with the given path.
        The resulting recipe is TODO
        """
        path = path.absolute()
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "conanfile.py", "w+") as file:

            # Process the Conan data into a Conan format
            name = SynodicPlugin.data["tool"]["poetry"]["name"]
            name = name.replace("-", "")

            dependencies = [
                "/".join(tup)
                for tup in SynodicPlugin.data["tool"]["conan"]["dependencies"].items()
            ]
            dependencies = ",".join('"{0}"'.format(w) for w in dependencies)

            generators = ",".join('"{0}"'.format(g) for g in SynodicPlugin.generators)

            # Write the Conan data to file
            contents = (
                f"from conans import ConanFile, CMake\n"
                f"\n"
                f"class {name}Conan(ConanFile):\n"
                f'    settings = "os", "compiler", "build_type", "arch"\n'
                f"    requires = {dependencies}\n"
                f"    generators = {generators}\n"
            )

            print(contents, file=file)

    def activate(self, poetry: _Poetry, io: _IO):
        """
        The entry function for the Poetry plugin
        """

        io.write_line(f"Hello")

    def poetry_new(self):

        pass

    def poetry_init(self):

        pass

    def poetry_install(self):

        _ConanAPI().install(
            path=SynodicPlugin.data["tool"]["conan"]["install-path"],
            name=SynodicPlugin.data["tool"]["poetry"]["name"],
            version=SynodicPlugin.data["tool"]["poetry"]["version"],
            user=None,
            channel=None,
            settings=None,
            options=None,
            env=None,
            remote_name=SynodicPlugin.data["tool"]["conan"]["remotes"],
            verify=None,
            manifests=None,
            manifests_interactive=None,
            build=None,
            profile_names=None,
            update=False,
            generators=None,
            no_imports=False,
            install_folder=SynodicPlugin.data["tool"]["conan"]["install-path"],
            cwd=_Path().absolute(),
            lockfile=None,
        )

    def poetry_update(self):

        _ConanAPI().install(
            path=SynodicPlugin.data["tool"]["conan"]["install-path"],
            name=SynodicPlugin.data["tool"]["poetry"]["name"],
            version=SynodicPlugin.data["tool"]["poetry"]["version"],
            user=None,
            channel=None,
            settings=None,
            options=None,
            env=None,
            remote_name=SynodicPlugin.data["tool"]["conan"]["remotes"],
            verify=None,
            manifests=None,
            manifests_interactive=None,
            build=None,
            profile_names=None,
            update=True,
            generators=None,
            no_imports=False,
            install_folder=SynodicPlugin.data["tool"]["conan"]["install-path"],
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
        """
        Validate the conan entries
        """

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

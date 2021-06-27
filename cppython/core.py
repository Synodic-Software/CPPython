from pathlib import Path
from abc import ABC, abstractmethod
from pydantic import BaseModel, AnyUrl, ValidationError
from pathlib import Path

import importlib
import pkgutil
import inspect

# TODO: Comment
import cppython.plugins


class Remote(BaseModel):
    name: str
    url = AnyUrl

class Version(BaseModel):
    version: str

class Dependency(BaseModel):
    name: str
    version = Version

class PEP621(BaseModel):
    """
    Subset of PEP 621
        The entirety of PEP 621 is not relevant for this plugin
        Link: https://www.python.org/dev/peps/pep-0621/
        TODO: Add additional info
    """

    name: str
    version: str
    description: str = ""


class Metadata(BaseModel):
    """
    TODO: Description
    """

    remotes: list[Remote] = []
    dependencies: list[Dependency] = []
    install_path: Path

class Plugin(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def valid(self, data: dict) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def gather_pep_612(self, data: dict) -> PEP621:
        raise NotImplementedError()


class Project:
    def __init__(self, path: Path, data: dict = {}) -> None:
        """
        data - The top level dictionary of the pyproject.toml file
                    If not provided, pyproject.toml will be loaded internally
        """

        self.enabled = False
        self.dirty = False

        # TODO: If data is loaded, it needs to be written out as well
        if not data:

            if path.is_file():
                path = path.parent

            while not path.glob("pyproject.toml"):
                if path.is_absolute():
                    assert "This is not a valid project. No pyproject.toml found in the current directory or any of its parents."

            import toml

            data = toml.load(path / "pyproject.toml")

        # Deactivate this plugin based on the presence of the 'conan' table
        if "tool" not in data or "conan" not in data["tool"]:
            return

        # import all plugins from the namespace

        def extract_plugin(namespace_package):
            for _, name, is_package in pkgutil.iter_modules(
                namespace_package.__path__, namespace_package.__name__ + "."
            ):
                if not is_package:
                    module = importlib.import_module(name)
                    class_members = inspect.getmembers(module, inspect.isclass)
                    for (_, value) in class_members:
                        if issubclass(value, Plugin) & (value is not Plugin):
                            plugin = value()
                            if plugin.valid(data):
                                return plugin
            return None

        project_plugin = extract_plugin(cppython.plugins)

        # This is not a valid project.
        if project_plugin is None:
            return

        # Pass-through initialization ends here
        self.enabled = True

        self.info = project_plugin.gather_pep_612(data)
        self.metadata = Metadata(**data["tool"]["conan"])


class _BaseGenerator:
    def __init__(self, project: Project) -> None:
        self._project = project


class ConanGenerator(_BaseGenerator):
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

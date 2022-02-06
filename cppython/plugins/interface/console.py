"""
TODO: 
"""

from pathlib import Path

import click
import tomlkit
from tomlkit.api import TOMLDocument

from cppython.project import Project
from cppython.schema import PEP621, Interface, PyProject


def _path_search() -> Path:
    """
    TODO
    """
    path = Path.cwd()

    while not path.glob("pyproject.toml"):
        if path.is_absolute():
            assert (
                False
            ), "This is not a valid project. No pyproject.toml found in the current directory or any of its parents."

    return Path(path / "pyproject.toml")


def _read_data(path: Path) -> TOMLDocument:
    """
    TODO
    """

    return tomlkit.loads(path.read_text(encoding="utf-8"))


class Config:
    """
    The data object that will be expanded alongside 'pass_obj'
    """

    def __init__(self):

        path = _path_search()
        data = _read_data(path)

        pyproject = PyProject(data=data, path=path)

        # Initialize the object hook into CPPython
        interface = ConsoleInterface(pyproject)

        # Initialize the CPPython context
        self.project = Project(interface)

    def load(self):
        """
        TODO
        """
        self.project.load()


pass_config = click.make_pass_decorator(Config)


@click.group()
@click.pass_context
def cli(context):
    """
    TODO
    """
    context.ensure_object(Config)

    # Initialize cppython
    context.obj.load()


@cli.command()
@pass_config
def install(config):
    """
    TODO
    """
    config.project.install()


@cli.command()
@pass_config
def update(config):
    """
    TODO
    """
    config.project.update()


@cli.result_callback()
@pass_config
def cleanup(config, result):
    """
    TODO
    """


class ConsoleInterface(Interface):
    """
    TODO: Description
    """

    def __init__(self, pyproject: PyProject) -> None:
        super().__init__(pyproject)

    # Plugin Contract

    @staticmethod
    def name() -> str:
        """
        The name of the generator
        """
        return "console"

    # Interface Contract

    @staticmethod
    def external_config() -> bool:
        """
        True if the plugin can read its own configuration.
        False otherwise
        """

        return False

    @staticmethod
    def parse_pep_621(data: PyProject) -> PEP621:
        """
        Requests the plugin to read the available PEP 621 information. Only requested if the plugin is not the entrypoint
        """
        raise NotImplementedError()

    def pep_621(self) -> PEP621:
        """
        Requests PEP 621 information from the pyproject
        """
        return self.parse_pep_621(self._pyproject)

    def write_pyproject(self) -> None:
        raise NotImplementedError()

    def read_pyproject(self) -> PyProject:
        return self._pyproject

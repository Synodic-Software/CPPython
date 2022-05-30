"""
A click CLI for CPPython interfacing
"""

from pathlib import Path
from typing import Any, Type

import click
import tomlkit
from cppython_core.schema import GeneratorDataT, Interface, InterfaceConfiguration

from cppython.console.vcs.git import Git
from cppython.project import Project, ProjectConfiguration


def _find_pyproject_file() -> Path:
    """
    TODO
    """

    # Search for a path upward
    path = Path.cwd()

    while not path.glob("pyproject.toml"):
        if path.is_absolute():
            assert (
                False
            ), "This is not a valid project. No pyproject.toml found in the current directory or any of its parents."

    path = Path(path)

    return path


def _create_pyproject(path: Path) -> dict[str, Any]:
    """
    TODO
    """

    # Load file
    data = tomlkit.loads(path.read_text(encoding="utf-8"))

    # Interpret and validate data
    return data


class Config:
    """
    The data object that will be expanded alongside 'pass_obj'
    """

    def __init__(self):
        path = _find_pyproject_file()
        self.pyproject_data = _create_pyproject(path / "pyproject.toml")

        configuration = InterfaceConfiguration()
        self.interface = ConsoleInterface(configuration)

        # TODO: Don't assume git SCM. Implement importing and scm selection

        version = Git().extract_version(path)
        self.configuration = ProjectConfiguration(root_path=path, version=version.base_version)

    def create_project(self) -> Project:
        """
        TODO
        """
        return Project(self.configuration, self.interface, self.pyproject_data)


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option("-v", "--verbose", count=True, help="Print additional output")
@pass_config
def cli(config, verbose: int):
    """
    entry_point group for the CLI commands
    """
    config.configuration.verbosity = verbose


@cli.command()
@pass_config
def info(config):
    """
    TODO
    """
    config.create_project()


@cli.command()
@pass_config
def install(config):
    """
    TODO
    """
    project = config.create_project()
    project.install()


@cli.command()
@pass_config
def update(config):
    """
    TODO
    """
    project = config.create_project()
    project.update()


@cli.command()
@pass_config
def build(config):
    """
    TODO
    """
    project = config.create_project()
    project.build()


class ConsoleInterface(Interface):
    """
    Interface implementation to pass to the project
    """

    def __init__(self, configuration: InterfaceConfiguration) -> None:
        super().__init__(configuration)

    @staticmethod
    def name() -> str:
        return "console"

    def read_generator_data(self, generator_data_type: Type[GeneratorDataT]) -> GeneratorDataT:
        """
        Requests generator information
        """
        return generator_data_type()

    def write_pyproject(self) -> None:
        """
        Write output
        """

"""
A click CLI for CPPython interfacing
"""

from pathlib import Path
from typing import Type
from xmlrpc.client import Boolean

import click
import tomlkit
from cppython_core.schema import GeneratorDataType, Interface, PyProject

from cppython.project import Project, ProjectConfiguration


def _create_pyproject():

    # Search for a path upward
    path = Path.cwd()

    while not path.glob("pyproject.toml"):
        if path.is_absolute():
            assert (
                False
            ), "This is not a valid project. No pyproject.toml found in the current directory or any of its parents."

    path = Path(path / "pyproject.toml")

    # Load file
    data = tomlkit.loads(path.read_text(encoding="utf-8"))

    # Interpret and validate data
    return PyProject(**data)


class Config:
    """
    The data object that will be expanded alongside 'pass_obj'
    """

    def __init__(self):
        self.pyproject = _create_pyproject()
        self.interface = ConsoleInterface()
        self.configuration = ProjectConfiguration()

    def create_project(self) -> Project:
        """
        TODO
        """
        return Project(self.configuration, self.interface, self.pyproject)


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Print additional output")
@pass_config
def cli(config, verbose: Boolean):
    """
    entry_point group for the CLI commands
    """
    config.configuration.verbose = verbose


@cli.command()
@pass_config
def info(config):
    """
    TODO
    """
    project = config.create_project()


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

    def read_generator_data(self, generator_data_type: Type[GeneratorDataType]) -> GeneratorDataType:
        """
        Requests generator information
        """
        return generator_data_type()

    def write_pyproject(self) -> None:
        """
        Write output
        """

    def print(self, string: str) -> None:
        """
        TODO
        """
        click.echo(string)

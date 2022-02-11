"""
TODO: 
"""

from pathlib import Path
from typing import Any, Type

import click
import tomlkit
from tomlkit.api import TOMLDocument

from cppython.project import Project
from cppython.schema import PEP621, CPPythonData, GeneratorData, Interface, PyProject


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

        # Initialize the object hook into CPPython
        interface = ConsoleInterface()

        # Initialize the CPPython context
        self.project = Project(interface)


pass_config = click.make_pass_decorator(Config)


@click.group()
@click.pass_context
def cli(context):
    """
    TODO
    """
    context.ensure_object(Config)


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

    # Interface Contract

    def generator_data(self, generator_data: Type[GeneratorData]) -> GeneratorData:
        """
        Requests generator information
        """
        raise NotImplementedError()

    def write_pyproject(self) -> None:
        raise NotImplementedError()

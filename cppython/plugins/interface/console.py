"""
A click CLI for CPPython interfacing
"""

from pathlib import Path
from typing import Type

import click
import tomlkit

from cppython.project import Project
from cppython.schema import GeneratorData, GeneratorDataType, Interface, PyProject


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
        pyproject = _create_pyproject()

        # Initialize the object hook into CPPython
        interface = ConsoleInterface(pyproject)

        # Initialize the CPPython context
        self.project = Project(interface)


pass_config = click.make_pass_decorator(Config)


@click.group()
@click.pass_context
def cli(context):
    """
    entry_point group for the CLI commands
    """
    context.ensure_object(Config)


@cli.command()
@pass_config
def install(config):
    """
    Fulfills the 'install' API requirement
    """
    config.project.install()


@cli.command()
@pass_config
def update(config):
    """
    Fulfills the 'update' API requirement
    """
    config.project.update()


@cli.command()
@pass_config
def build(config):
    """
    Fulfills the 'build' API requirement
    """
    config.project.build()


@cli.result_callback()
@pass_config
def cleanup(config, result):
    """
    Post-command cleanup
    """


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
        pass

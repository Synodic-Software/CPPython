"""A click CLI for CPPython interfacing
"""

from logging import getLogger
from pathlib import Path

import click
import tomlkit
from cppython_core.plugin_schema.interface import Interface
from cppython_core.plugin_schema.vcs import VersionControl
from cppython_core.schema import ProjectConfiguration

from cppython.builder import InterfaceBuilder
from cppython.project import Project


def _find_pyproject_file() -> Path:
    """Searches upward for a pyproject.toml file

    Returns:
        The found directory
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


class Configuration:
    """Click configuration object"""

    def __init__(self) -> None:
        path = _find_pyproject_file()
        file_path = path / "pyproject.toml"
        self.pyproject_data = tomlkit.loads(file_path.read_text(encoding="utf-8"))

        self.interface = ConsoleInterface()

        self.logger = getLogger("cppython.console")
        builder = InterfaceBuilder(self.logger)

        if not (vcs_types := builder.discover_vcs()):
            raise TypeError("No VCS plugin found")

        plugin = None
        for vcs_type in vcs_types:
            vcs = builder.create_vcs(
                vcs_type,
            )
            if vcs.is_repository(path):
                plugin = vcs
                break

        if not plugin:
            raise TypeError("No applicable VCS plugin found for the given path")

        version = plugin.extract_version(path)

        self.configuration = ProjectConfiguration(pyproject_file=file_path, version=version)
        self.project = Project(self.configuration, self.interface, self.pyproject_data)

    def query_vcs(self) -> str:
        """Queries the VCS system for its version

        Returns:
            The version
        """

        return "TODO"


# Attach our config object to click's hook
pass_config = click.make_pass_decorator(Configuration, ensure=True)


@click.group()
@click.option("-v", "--verbose", count=True, help="Print additional output")
@pass_config
def cli(config: Configuration, verbose: int) -> None:
    """entry_point group for the CLI commands

    Args:
        config: The CLI configuration object
        verbose: The verbosity level
    """
    config.configuration.verbosity = verbose


@cli.command()
@pass_config
def info(config: Configuration) -> None:
    """Prints project information

    Args:
        config: The CLI configuration object
    """

    version = config.query_vcs()
    config.logger.info("The VCS project version is: %s", version)


@cli.command()
@pass_config
def install(config: Configuration) -> None:
    """Install API call

    Args:
        config: The CLI configuration object
    """
    config.project.install()


@cli.command()
@pass_config
def update(config: Configuration) -> None:
    """Update API call

    Args:
        config: The CLI configuration object
    """
    config.project.update()


class ConsoleInterface(Interface):
    """Interface implementation to pass to the project"""

    @staticmethod
    def name() -> str:
        """Returns the name of the interface

        Returns:
            The name
        """
        return "console"

    def write_pyproject(self) -> None:
        """Write output"""

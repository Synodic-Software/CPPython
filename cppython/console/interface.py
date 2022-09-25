"""A click CLI for CPPython interfacing
"""

from logging import getLogger
from pathlib import Path

import click
import tomlkit
from cppython_core.schema import (
    Interface,
    InterfaceConfiguration,
    ProjectConfiguration,
    ProviderDataT,
    VersionControl,
)

from cppython.builder import PluginBuilder
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

        configuration = InterfaceConfiguration()
        self.interface = ConsoleInterface(configuration)

        plugin_builder = PluginBuilder("version_control", getLogger())

        # Don't filter entries
        entries = plugin_builder.gather_entries()
        vcs_types = plugin_builder.load(entries)

        plugins: list[type[VersionControl]] = []

        # Verify the plugin type
        for vcs_type in vcs_types:
            if not issubclass(vcs_type, VersionControl):
                raise TypeError("The VCS plugin must be an instance of VersionControl")

            plugins.append(vcs_type)

        # Extract the first plugin that identifies the repository
        plugin = None
        for plugin_type in plugins:
            plugin = plugin_type()
            plugin.is_repository(path)
            break

        if plugin is None:
            raise TypeError("No VCS plugin found")

        version = plugin.extract_version(path)
        self.configuration = ProjectConfiguration(pyproject_file=file_path, version=version)

    def create_project(self) -> Project:
        """Creates the project type from input data

        Returns:
            The project
        """
        return Project(self.configuration, self.interface, self.pyproject_data)

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
    config.create_project()


@cli.command()
@pass_config
def install(config: Configuration) -> None:
    """Install API call

    Args:
        config: The CLI configuration object
    """
    project = config.create_project()
    project.install()


@cli.command()
@pass_config
def update(config: Configuration) -> None:
    """Update API call

    Args:
        config: The CLI configuration object
    """
    project = config.create_project()
    project.update()


class ConsoleInterface(Interface):
    """Interface implementation to pass to the project"""

    @staticmethod
    def name() -> str:
        """Returns the name of the interface

        Returns:
            The name
        """
        return "console"

    def read_provider_data(self, provider_data_type: type[ProviderDataT]) -> ProviderDataT:
        """Requests provider information

        Args:
            provider_data_type: The type to construct

        Returns:
            The constructed provider data type
        """
        return provider_data_type()

    def write_pyproject(self) -> None:
        """Write output"""

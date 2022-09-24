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
    """_summary_

    Returns:
        _description_
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
        self.configuration = ProjectConfiguration(pyproject_file=file_path, version=version.base_version)

    def create_project(self) -> Project:
        """_summary_

        Returns:
            _description_
        """
        return Project(self.configuration, self.interface, self.pyproject_data)

    def query_vcs(self) -> str:
        """_summary_

        Returns:
            _description_
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
        config: _description_
        verbose: _description_
    """
    config.configuration.verbosity = verbose


@cli.command()
@pass_config
def info(config: Configuration) -> None:
    """_summary_

    Args:
        config: _description_
    """
    config.create_project()


@cli.command()
@pass_config
def install(config: Configuration) -> None:
    """_summary_

    Args:
        config: _description_
    """
    project = config.create_project()
    project.install()


@cli.command()
@pass_config
def update(config: Configuration) -> None:
    """_summary_

    Args:
        config: _description_
    """
    project = config.create_project()
    project.update()


class ConsoleInterface(Interface):
    """Interface implementation to pass to the project

    Args:
        Interface: _description_
    """

    @staticmethod
    def name() -> str:
        """_summary_

        Returns:
            _description_
        """
        return "console"

    def read_provider_data(self, provider_data_type: type[ProviderDataT]) -> ProviderDataT:
        """Requests provider information

        Args:
            provider_data_type: _description_

        Returns:
            _description_
        """
        return provider_data_type()

    def write_pyproject(self) -> None:
        """Write output"""

"""Everything needed to build a CPPython project
"""

from importlib import metadata
from logging import Logger
from pathlib import Path
from typing import Any

from cppython_core.exceptions import ConfigError
from cppython_core.plugin_schema.generator import Generator, GeneratorT
from cppython_core.plugin_schema.provider import Provider, ProviderT
from cppython_core.plugin_schema.vcs import VersionControl
from cppython_core.resolution import (
    resolve_cppython,
    resolve_cppython_plugin,
    resolve_generator,
    resolve_pep621,
    resolve_project_configuration,
    resolve_provider,
)
from cppython_core.schema import (
    CoreData,
    CorePluginData,
    CPPythonGlobalConfiguration,
    CPPythonLocalConfiguration,
    PEP621Configuration,
    Plugin,
    ProjectConfiguration,
)


class PluginBuilder:
    """Collection of utilities to collect and build plugins"""

    def __init__(self, group: str, logger: Logger) -> None:
        self._group = group
        self._logger = logger

    def gather_entries(self) -> list[metadata.EntryPoint]:
        """Gather all the available entry points for the grouping

        Returns:
            List of entries
        """
        return list(metadata.entry_points(group=f"cppython.{self._group}"))

    def load(self, entry_points: list[metadata.EntryPoint]) -> list[type[Plugin]]:
        """Loads a set of entry points

        Args:
            entry_points: The entry points to load

        Raises:
            TypeError: If an entry point is not a subclass of the 'Plugin' type

        Returns:
            List of plugin types
        """

        plugins = []

        for entry_point in entry_points:
            plugin = entry_point.load()

            if not issubclass(plugin, Plugin):
                raise TypeError("The CPPython plugin must be an instance of Plugin")

            plugins.append(plugin)

        return plugins


class Builder:
    """Helper class for building CPPython projects"""

    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def generate_core_data(
        self,
        configuration: ProjectConfiguration,
        pep621_configuration: PEP621Configuration,
        cppython_configuration: CPPythonLocalConfiguration,
    ) -> CoreData:
        """_summary_

        Args:
            self: _description_
            configuration: TODO
            pep621_configuration: TODO
            cppython_configuration: TODO

        Raises:
            ConfigError: Raised if data cannot be parsed

        Returns:
            _description_
        """

        global_configuration = CPPythonGlobalConfiguration()

        project_data = resolve_project_configuration(configuration)

        try:
            pep621_data = resolve_pep621(pep621_configuration, configuration)

        except ConfigError:
            configuration.version = self.extract_vcs_version(configuration.pyproject_file.parent)
            pep621_data = resolve_pep621(pep621_configuration, configuration)

        cppython_data = resolve_cppython(cppython_configuration, global_configuration, project_data)

        return CoreData(project_data=project_data, pep621_data=pep621_data, cppython_data=cppython_data)

    def extract_vcs_version(self, path: Path) -> str:
        """_summary_

        Args:
            path: _description_

        Raises:
            TypeError: _description_
            TypeError: _description_

        Returns:
            _description_
        """

        if not (vcs_types := self.discover_vcs()):
            raise TypeError("No VCS plugin found")

        plugin = None
        for vcs_type in vcs_types:
            vcs = vcs_type()
            if vcs.is_repository(path):
                plugin = vcs
                break

        if not plugin:
            raise TypeError("No applicable VCS plugin found for the given path")

        return plugin.extract_version(path)

    def discover_providers(self) -> list[type[Provider]]:
        """Discovers plugin types
        Raises:
            TypeError: Raised if the Plugin type is not subclass of 'Provider'

        Returns:
            List of Provider types
        """
        provider_builder = PluginBuilder(Provider.group(), self.logger)

        # Gather provider entry points without any filtering
        provider_entry_points = provider_builder.gather_entries()
        provider_types = provider_builder.load(provider_entry_points)

        plugins = []

        for provider_type in provider_types:
            if not issubclass(provider_type, Provider):
                raise TypeError("The CPPython plugin must be an instance of Plugin")

            plugins.append(provider_type)

        return plugins

    def discover_generators(self) -> list[type[Generator]]:
        """Discovers plugin types
        Raises:
            TypeError: Raised if the Plugin type is not subclass of 'Generator'

        Returns:
            List of Generator types
        """
        generator_builder = PluginBuilder(Generator.group(), self.logger)

        # Gather generator entry points without any filtering
        generator_entry_points = generator_builder.gather_entries()
        generator_types = generator_builder.load(generator_entry_points)

        plugins = []

        for generator_type in generator_types:
            if not issubclass(generator_type, Generator):
                raise TypeError("The CPPython plugin must be an instance of Plugin")

            plugins.append(generator_type)

        return plugins

    def discover_vcs(self) -> list[type[VersionControl]]:
        """Discovers plugin types
        Raises:
            TypeError: Raised if the Plugin type is not subclass of 'VersionControl'

        Returns:
            List of VersionControl types
        """
        vcs_builder = PluginBuilder(VersionControl.group(), self.logger)

        # Gather vcs entry points without any filtering
        vcs_entry_points = vcs_builder.gather_entries()
        vcs_types = vcs_builder.load(vcs_entry_points)

        plugins = []

        for vcs_type in vcs_types:
            if not issubclass(vcs_type, VersionControl):
                raise TypeError("The CPPython plugin must be an instance of Plugin")

            plugins.append(vcs_type)

        return plugins

    def create_generator(
        self, plugin_types: list[type[GeneratorT]], core_data: CoreData, generator_configuration: dict[str, Any]
    ) -> GeneratorT:
        """_summary_

        Args:
            plugin_types: _description_
            core_data: _description_
            generator_configuration: TODO

        Raises:
            ConfigError: TODO

        Returns:
            _description_
        """

        plugin_type, table = None, None
        # Extract the first type that's readable
        for plugin_type in plugin_types:
            name = plugin_type.name()

            try:
                table = generator_configuration[name]
                break
            except KeyError:
                continue

        if plugin_type is None:
            raise ConfigError("plugin_types was empty")

        if table is None:
            raise ConfigError("No generator name found within the 'tool.cppython.generator' table")

        generator_data = resolve_generator(core_data.project_data)

        cppython_plugin_data = resolve_cppython_plugin(core_data.cppython_data, plugin_type)

        core_plugin_data = CorePluginData(
            project_data=core_data.project_data,
            pep621_data=core_data.pep621_data,
            cppython_data=cppython_plugin_data,
        )

        return plugin_type(generator_data, core_plugin_data, table)

    def create_providers(
        self, plugin_types: list[type[ProviderT]], core_data: CoreData, provider_configuration: dict[str, Any]
    ) -> list[ProviderT]:
        """Creates Providers from input data

        Args:
            plugin_types: TODO
            core_data: TODO
            provider_configuration: TODO

        Returns:
            TODO
        """

        plugins = []

        for plugin_type in plugin_types:
            name = plugin_type.name()
            table = provider_configuration[name]

            provider_data = resolve_provider(core_data.project_data)

            cppython_plugin_data = resolve_cppython_plugin(core_data.cppython_data, plugin_type)

            core_plugin_data = CorePluginData(
                project_data=core_data.project_data,
                pep621_data=core_data.pep621_data,
                cppython_data=cppython_plugin_data,
            )

            plugins.append(plugin_type(provider_data, core_plugin_data, table))

        return plugins

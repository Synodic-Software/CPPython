"""Everything needed to build a CPPython project
"""

from dataclasses import dataclass
from importlib import metadata
from logging import Logger
from pathlib import Path
from typing import Any, Generic

from cppython_core.exceptions import ConfigError, PluginError
from cppython_core.plugin_schema.generator import Generator
from cppython_core.plugin_schema.provider import Provider
from cppython_core.plugin_schema.scm import SCM
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
    DataPlugin,
    PEP621Configuration,
    Plugin,
    PluginT,
    ProjectConfiguration,
)


class PluginBuilder(Generic[PluginT]):
    """Collection of utilities to collect and build plugins"""

    def __init__(self, plugin_type: type[PluginT], logger: Logger) -> None:
        self._plugin_type = plugin_type
        self._group = plugin_type.group()
        self._logger = logger

    def gather_entries(self) -> list[metadata.EntryPoint]:
        """Gather all the available entry points for the grouping

        Returns:
            List of entries
        """
        return list(metadata.entry_points(group=f"cppython.{self._group}"))

    def load(self, entry_points: list[metadata.EntryPoint]) -> list[type[PluginT]]:
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
                raise TypeError(f"The '{type(plugin).__name__}' plugin must be an instance of 'Plugin'")

            if not issubclass(plugin, self._plugin_type):
                raise TypeError(f"The '{type(plugin).__name__}' plugin must be an instance of '{self._group}'")

            plugins.append(plugin)

        return plugins


@dataclass
class PluginInformation:
    """Data that the builder outputs about plugins"""

    plugin_type: type[DataPlugin[Any]]
    entry: metadata.EntryPoint


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
        """Parses and returns resolved data from all configuration sources

        Args:
            configuration: Input configuration
            pep621_configuration: Project table configuration
            cppython_configuration: Tool configuration

        Raises:
            ConfigError: Raised if data cannot be parsed

        Returns:
            The resolved core object
        """

        global_configuration = CPPythonGlobalConfiguration()

        project_data = resolve_project_configuration(configuration)

        try:
            pep621_data = resolve_pep621(pep621_configuration, configuration)

        except ConfigError:
            configuration.version = self.extract_scm_version(configuration.pyproject_file.parent)
            pep621_data = resolve_pep621(pep621_configuration, configuration)

        cppython_data = resolve_cppython(cppython_configuration, global_configuration, project_data)

        return CoreData(project_data=project_data, pep621_data=pep621_data, cppython_data=cppython_data)

    def extract_scm_version(self, path: Path) -> str:
        """Locates an available SCM plugin that can report version information about the given path

        Args:
            path: The directory to query

        Raises:
            PluginError: If no SCM plugin can be found

        Returns:
            A version token
        """

        scm_builder = PluginBuilder(SCM, self.logger)
        entries = scm_builder.gather_entries()
        scm_types = scm_builder.load(entries)

        if not entries:
            raise PluginError("No SCM plugin found")

        plugin = None
        for scm_type, entry in zip(scm_types, entries):
            scm = scm_type(entry)
            if scm.is_repository(path):
                plugin = scm
                break

        if not plugin:
            raise PluginError("No applicable SCM plugin found for the given path")

        return plugin.extract_version(path)

    def find_generator(self, core_data: CoreData) -> PluginInformation:
        generator_builder = PluginBuilder(Generator, self.logger)
        entries = generator_builder.gather_entries()

        if not (generator_types := generator_builder.load(entries)):
            raise PluginError("No generator plugin was found")

        for generator_type in generator_types:
            self.logger.warning("Generator plugin found: %s", generator_type.name())

        # Lookup the requested generator if given
        supported_plugin_type = None
        supported_plugin_entry = None
        if core_data.cppython_data.generator_name is not None:
            for plugin_type, entry in zip(generator_types, entries):
                if plugin_type.name() == core_data.cppython_data.generator_name:
                    supported_plugin_type = plugin_type
                    supported_plugin_entry = entry
                    break

        # Try and deduce generator
        if supported_plugin_type is None:
            for plugin_type, entry in zip(generator_types, entries):
                if plugin_type.supported(core_data.project_data.pyproject_file.parent):
                    supported_plugin_type = plugin_type
                    supported_plugin_entry = entry
                    break

        # Fail
        if supported_plugin_type is None or supported_plugin_entry is None:
            raise PluginError(
                "The 'generator_name' was empty and no generator could be deduced from the root directory."
            )

        self.logger.warning("Using generator plugin: '%s'", supported_plugin_type.name())

        return PluginInformation(plugin_type=supported_plugin_type, entry=supported_plugin_entry)

    def create_generator(
        self, core_data: CoreData, generator_configuration: dict[str, Any], plugin_info: PluginInformation
    ) -> Generator:
        """Creates a generator from input configuration

        Args:
            core_data: The resolved configuration data
            generator_configuration: The generator table of the CPPython configuration data

        Raises:
            PluginError: Raised if no viable generator plugin was found

        Returns:
            The constructed generator
        """

        generator_data = resolve_generator(core_data.project_data)

        cppython_plugin_data = resolve_cppython_plugin(core_data.cppython_data, plugin_info.plugin_type)

        core_plugin_data = CorePluginData(
            project_data=core_data.project_data,
            pep621_data=core_data.pep621_data,
            cppython_data=cppython_plugin_data,
        )

        plugin = plugin_info.plugin_type(plugin_info.entry, generator_data, core_plugin_data)

        if not generator_configuration:
            self.logger.error(
                "The pyproject.toml table 'tool.cppython.generator' does not exist. Sending generator empty data",
            )

        plugin.activate(generator_configuration)

        return plugin

    def create_provider(self, core_data: CoreData, provider_configuration: dict[str, Any]) -> Provider:
        """Creates Providers from input data

        Args:
            core_data: The resolved configuration data
            provider_configuration: The provider data table

        Raises:
            PluginError: Raised if no viable generator plugin was found

        Returns:
            A constructed provider plugins
        """

        provider_builder = PluginBuilder(Provider, self.logger)
        entries = provider_builder.gather_entries()

        if not (provider_types := provider_builder.load(entries)):
            raise PluginError("No provider plugin was found")

        for provider_type in provider_types:
            self.logger.warning("Provider plugin found: %s", provider_type.name())

        # Lookup the requested generator if given
        supported_plugin_type = None
        supported_plugin_entry = None
        if core_data.cppython_data.provider_name is not None:
            for plugin_type, entry in zip(provider_types, entries):
                if plugin_type.name() == core_data.cppython_data.provider_name:
                    supported_plugin_type = plugin_type
                    supported_plugin_entry = entry
                    break

        # Try and deduce generator
        if supported_plugin_type is None:
            for plugin_type, entry in zip(provider_types, entries):
                if plugin_type.supported(core_data.project_data.pyproject_file.parent):
                    supported_plugin_type = plugin_type
                    supported_plugin_entry = entry
                    break

        # Fail
        if supported_plugin_type is None:
            raise PluginError(
                "The 'provider_name' was empty and no generator could be deduced from the root directory."
            )

        self.logger.warning("Using generator plugin: '%s'", supported_plugin_type.name())

        provider_data = resolve_provider(core_data.project_data, core_data.cppython_data)

        cppython_plugin_data = resolve_cppython_plugin(core_data.cppython_data, supported_plugin_type)

        core_plugin_data = CorePluginData(
            project_data=core_data.project_data,
            pep621_data=core_data.pep621_data,
            cppython_data=cppython_plugin_data,
        )

        plugin = supported_plugin_type(supported_plugin_entry, provider_data, core_plugin_data)

        plugin.activate(provider_configuration)

        return plugin

"""Everything needed to build a CPPython project
"""

from dataclasses import dataclass
from importlib import metadata
from logging import Logger
from pathlib import Path
from typing import Any

from cppython_core.exceptions import ConfigError, PluginError
from cppython_core.plugin_schema.generator import Generator
from cppython_core.plugin_schema.provider import Provider
from cppython_core.plugin_schema.scm import SCM
from cppython_core.resolution import (
    resolve_cppython,
    resolve_cppython_plugin,
    resolve_generator,
    resolve_name,
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
    ProjectConfiguration,
)


@dataclass
class GeneratorInformation:
    """Data that the builder outputs about plugins"""

    plugin_type: type[Generator]
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

        group = "SCM"

        scm_types: list[type[SCM]] = []

        if not (entries := list(metadata.entry_points(group=f"cppython.{group}"))):
            raise PluginError("No SCM plugin found")

        # Filter entries
        for entry_point in entries:
            plugin_type = entry_point.load()
            if not issubclass(plugin_type, SCM):
                self.logger.warning(
                    f"Found incompatible plugin. The '{resolve_name(plugin_type)}' plugin must be an instance of"
                    f" '{group}'"
                )
            else:
                scm_types.append(plugin_type)

        # Deduce the SCM repository
        plugin = None
        for scm_type in scm_types:
            scm = scm_type()
            if scm.supported(path):
                plugin = scm
                break

        if not plugin:
            raise PluginError("No applicable SCM plugin found for the given path")

        if (version := plugin.version(path)) is None:
            raise PluginError("Project has no version information")

        return version

    def find_generator(self, core_data: CoreData) -> GeneratorInformation:
        """_summary_

        Args:
            core_data: _description_

        Raises:
            PluginError: _description_

        Returns:
            _description_
        """

        group = "Generator"
        generator_info: list[tuple[type[Generator], metadata.EntryPoint]] = []

        # Filter entries
        for entry_point in list(metadata.entry_points(group=f"cppython.{group}")):
            plugin_type = entry_point.load()
            if not issubclass(plugin_type, Generator):
                self.logger.warning(
                    f"Found incompatible plugin. The '{type(plugin_type).__name__}' plugin must be an instance of"
                    f" '{group}'"
                )
            else:
                self.logger.warning("Generator plugin found: %s", resolve_name(plugin_type))
                generator_info.append((plugin_type, entry_point))

        if not generator_info:
            raise PluginError("No generator plugin was found")

        # Lookup the requested generator if given
        supported_plugin_info = None
        if core_data.cppython_data.generator_name is not None:
            for plugin_type, entry in generator_info:
                if resolve_name(plugin_type) == core_data.cppython_data.generator_name:
                    supported_plugin_info = plugin_type, entry
                    break

        # Try and deduce generator
        if supported_plugin_info is None:
            for plugin_type, entry in generator_info:
                if plugin_type.supported(core_data.project_data.pyproject_file.parent):
                    supported_plugin_info = plugin_type, entry
                    break

        # Fail
        if supported_plugin_info is None:
            raise PluginError(
                "The 'generator_name' was empty and no generator could be deduced from the root directory."
            )

        supported_plugin_type, supported_plugin_entry = supported_plugin_info
        self.logger.warning("Using generator plugin: '%s'", resolve_name(supported_plugin_type))

        return GeneratorInformation(plugin_type=supported_plugin_type, entry=supported_plugin_entry)

    def create_generator(
        self, core_data: CoreData, generator_configuration: dict[str, Any], plugin_info: GeneratorInformation
    ) -> Generator:
        """Creates a generator from input configuration

        Args:
            core_data: The resolved configuration data
            generator_configuration: The generator table of the CPPython configuration data
            plugin_info: The plugin information

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

        if not generator_configuration:
            self.logger.error(
                "The pyproject.toml table 'tool.cppython.generator' does not exist. Sending generator empty data",
            )

        return plugin_info.plugin_type(generator_data, core_plugin_data, generator_configuration)

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

        group = "Provider"

        entries = list(metadata.entry_points(group=f"cppython.{group}"))
        provider_info: list[type[Provider]] = []

        # Filter entries
        for entry_point in entries:
            plugin_type = entry_point.load()
            if not issubclass(plugin_type, Provider):
                self.logger.warning(
                    f"Found incompatible plugin. The '{resolve_name(plugin_type)}' plugin must be an instance of"
                    f" '{group}'"
                )
            else:
                self.logger.warning("Provider plugin found: %s", resolve_name(plugin_type))
                provider_info.append(plugin_type)

        if not provider_info:
            raise PluginError("No provider_types plugin was found")

        # Lookup the requested provider if given
        supported_plugin_type: type[Provider] | None = None
        if core_data.cppython_data.provider_name is not None:
            for plugin_type in provider_info:
                if resolve_name(plugin_type) == core_data.cppython_data.provider_name:
                    supported_plugin_type = plugin_type
                    break

        # Try and deduce provider
        if supported_plugin_type is None:
            for plugin_type in provider_info:
                if plugin_type.supported(core_data.project_data.pyproject_file.parent):
                    supported_plugin_type = plugin_type
                    break

        # Fail
        if supported_plugin_type is None:
            raise PluginError("The 'provider_name' was empty and no provider could be deduced from the root directory.")

        self.logger.warning("Using provider plugin: '%s'", resolve_name(supported_plugin_type))

        provider_data = resolve_provider(core_data.project_data, core_data.cppython_data)

        cppython_plugin_data = resolve_cppython_plugin(core_data.cppython_data, supported_plugin_type)

        core_plugin_data = CorePluginData(
            project_data=core_data.project_data,
            pep621_data=core_data.pep621_data,
            cppython_data=cppython_plugin_data,
        )

        if not provider_configuration:
            self.logger.error(
                "The pyproject.toml table 'tool.cppython.provider' does not exist. Sending provider empty data",
            )

        return supported_plugin_type(provider_data, core_plugin_data, provider_configuration)

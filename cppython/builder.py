"""Everything needed to build a CPPython project
"""

from importlib import metadata
from inspect import getmodule
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
    DataPluginT,
    PEP621Configuration,
    ProjectConfiguration,
)


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
        group_lower = group.lower()

        scm_types: list[type[SCM]] = []

        if not (entries := list(metadata.entry_points(group=f"cppython.{group_lower}"))):
            raise PluginError("No SCM plugin found")

        # Filter entries
        for entry_point in entries:
            plugin_type = entry_point.load()
            if not issubclass(plugin_type, SCM):
                self.logger.warning(
                    f"Found incompatible plugin. The '{resolve_name(plugin_type)}' plugin must be an instance of"
                    f" '{group_lower}'"
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

    def find_generators(self) -> list[type[Generator]]:
        """_summary_

        Raises:
            PluginError: _description_

        Returns:
            _description_
        """

        group_name = "generator"
        plugin_types: list[type[Generator]] = []

        # Filter entries by type
        for entry_point in list(metadata.entry_points(group=f"cppython.{group_name}")):
            loaded_type = entry_point.load()
            if not issubclass(loaded_type, Generator):
                self.logger.warning(
                    f"Found incompatible plugin. The '{resolve_name(loaded_type)}' plugin must be an instance of"
                    f" '{group_name}'"
                )
            else:
                self.logger.warning(
                    f"{group_name} plugin found: {resolve_name(loaded_type)} from {getmodule(loaded_type)}"
                )
                plugin_types.append(loaded_type)

        if not plugin_types:
            raise PluginError(f"No {group_name} plugin was found")

        return plugin_types

    def find_providers(self) -> list[type[Provider]]:
        """_summary_

        Raises:
            PluginError: _description_

        Returns:
            _description_
        """

        group_name = "provider"
        plugin_types: list[type[Provider]] = []

        # Filter entries by type
        for entry_point in list(metadata.entry_points(group=f"cppython.{group_name}")):
            loaded_type = entry_point.load()
            if not issubclass(loaded_type, Provider):
                self.logger.warning(
                    f"Found incompatible plugin. The '{resolve_name(loaded_type)}' plugin must be an instance of"
                    f" '{group_name}'"
                )
            else:
                self.logger.warning(
                    f"{group_name} plugin found: {resolve_name(loaded_type)} from {getmodule(loaded_type)}"
                )
                plugin_types.append(loaded_type)

        if not plugin_types:
            raise PluginError(f"No {group_name} plugin was found")

        return plugin_types

    def filter_plugins(
        self, plugin_types: list[type[DataPluginT]], directory: Path, pinned_name: str | None, group_name: str
    ) -> list[type[DataPluginT]]:
        """Finds and filters data plugins

        Args:
            plugin_types: The plugin type to lookup
            directory: The data to query support for the filtered plugins
            pinned_name: The configuration name
            group_name: The group name

        Raises:
            PluginError: Raised if no plugins can be found

        Returns:
            The list of applicable plugins
        """

        # Lookup the requested plugin if given
        if pinned_name is not None:
            for loaded_type in plugin_types:
                if resolve_name(loaded_type) == pinned_name:
                    self.logger.warning(
                        f"Using {group_name} plugin: {resolve_name(loaded_type)} from {getmodule(loaded_type)}"
                    )
                    return [loaded_type]

        self.logger.warning(f"'{group_name}_name' was empty. Trying to deduce {group_name}s")

        supported_types: list[type[DataPluginT]] = []

        # Deduce types
        for loaded_type in plugin_types:
            if loaded_type.supported(directory):
                self.logger.warning(
                    f"A {group_name} plugin is supported: {resolve_name(loaded_type)} from {getmodule(loaded_type)}"
                )
                supported_types.append(loaded_type)

        # Fail
        if supported_types is None:
            raise PluginError(f"No {group_name} could be deduced from the root directory.")

        return supported_types

    def solve(
        self, generator_types: list[type[Generator]], provider_types: list[type[Provider]]
    ) -> tuple[type[Generator], type[Provider]]:
        """_summary_

        Args:
            generator_types: _description_
            provider_types: _description_

        Raises:
            PluginError: _description_

        Returns:
            _description_
        """

        combos: list[tuple[type[Generator], type[Provider]]] = []

        for generator_type in generator_types:
            sync_types = generator_type.sync_types()
            for provider_type in provider_types:
                for sync_type in sync_types:
                    if provider_type.supported_sync_type(sync_type):
                        combos.append((generator_type, provider_type))
                        break

        if not combos:
            raise PluginError("No provider that supports a given generator could be deduced")

        return combos[0]

    def create_generator(
        self, core_data: CoreData, generator_configuration: dict[str, Any], generator_type: type[Generator]
    ) -> Generator:
        """Creates a generator from input configuration

        Args:
            core_data: The resolved configuration data
            generator_configuration: The generator table of the CPPython configuration data
            generator_type: The plugin type

        Raises:
            PluginError: Raised if no viable generator plugin was found

        Returns:
            The constructed generator
        """

        generator_data = resolve_generator(core_data.project_data)
        cppython_plugin_data = resolve_cppython_plugin(core_data.cppython_data, generator_type)

        core_plugin_data = CorePluginData(
            project_data=core_data.project_data,
            pep621_data=core_data.pep621_data,
            cppython_data=cppython_plugin_data,
        )

        if not generator_configuration:
            self.logger.error(
                "The pyproject.toml table 'tool.cppython.generator' does not exist. Sending generator empty data",
            )

        return generator_type(generator_data, core_plugin_data, generator_configuration)

    def create_provider(
        self, core_data: CoreData, provider_configuration: dict[str, Any], provider_type: type[Provider]
    ) -> Provider:
        """Creates Providers from input data

        Args:
            core_data: The resolved configuration data
            provider_configuration: The provider data table
            provider_type: The type to instantiate

        Raises:
            PluginError: Raised if no viable provider plugin was found

        Returns:
            A constructed provider plugins
        """

        provider_data = resolve_provider(core_data.project_data)
        cppython_plugin_data = resolve_cppython_plugin(core_data.cppython_data, provider_type)

        core_plugin_data = CorePluginData(
            project_data=core_data.project_data,
            pep621_data=core_data.pep621_data,
            cppython_data=cppython_plugin_data,
        )

        if not provider_configuration:
            self.logger.error(
                "The pyproject.toml table 'tool.cppython.provider' does not exist. Sending provider empty data",
            )

        return provider_type(provider_data, core_plugin_data, provider_configuration)

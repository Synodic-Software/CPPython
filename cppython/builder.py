"""Everything needed to build a CPPython project"""

import logging
from importlib import metadata
from inspect import getmodule
from logging import Logger
from typing import Any

from cppython_core.exceptions import PluginError
from cppython_core.plugin_schema.generator import Generator
from cppython_core.plugin_schema.provider import Provider
from cppython_core.plugin_schema.scm import SCM
from cppython_core.resolution import (
    PluginBuildData,
    PluginCPPythonData,
    resolve_cppython,
    resolve_cppython_plugin,
    resolve_generator,
    resolve_pep621,
    resolve_project_configuration,
    resolve_provider,
    resolve_scm,
)
from cppython_core.schema import (
    CoreData,
    CorePluginData,
    CPPythonGlobalConfiguration,
    CPPythonLocalConfiguration,
    DataPlugin,
    PEP621Configuration,
    PEP621Data,
    ProjectConfiguration,
    ProjectData,
)

from cppython.data import Data, Plugins


class Builder:
    """Helper class for building CPPython projects"""

    def __init__(self, project_configuration: ProjectConfiguration, logger: Logger) -> None:
        self.project_configuration = project_configuration
        self.logger = logger

        # Default logging levels
        levels = [logging.WARNING, logging.INFO, logging.DEBUG]

        # Add default output stream
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(levels[project_configuration.verbosity])

        self.logger.info("Logging setup complete")

    def _generate_plugins(
        self, local_configuration: CPPythonLocalConfiguration, project_data: ProjectData
    ) -> PluginBuildData:
        """_summary_

        Args:
            local_configuration: _description_
            project_data: _description_

        Returns:
            _description_
        """

        raw_generator_plugins = self._find_generators()
        generator_plugins = self._filter_plugins(
            raw_generator_plugins,
            local_configuration.generator_name,
            "Generator",
        )

        raw_provider_plugins = self._find_providers()
        provider_plugins = self._filter_plugins(
            raw_provider_plugins,
            local_configuration.provider_name,
            "Provider",
        )

        scm_plugins = self._find_source_managers()

        scm_type = self._select_scm(scm_plugins, project_data)

        # Solve the messy interactions between plugins
        generator_type, provider_type = self._solve(generator_plugins, provider_plugins)

        return PluginBuildData(generator_type=generator_type, provider_type=provider_type, scm_type=scm_type)

    def _generate_cppython_plugin_data(self, plugin_build_data: PluginBuildData) -> PluginCPPythonData:
        """Generates the CPPython plugin data from the resolved plugins

        Args:
            plugin_build_data: The resolved plugin data

        Returns:
            The plugin data used by CPPython
        """

        return PluginCPPythonData(
            generator_name=plugin_build_data.generator_type.name(),
            provider_name=plugin_build_data.provider_type.name(),
            scm_name=plugin_build_data.scm_type.name(),
        )

    def _generate_pep621_data(
        self, pep621_configuration: PEP621Configuration, project_configuration: ProjectConfiguration, scm: SCM | None
    ) -> PEP621Data:
        """_summary_

        Args:
            pep621_configuration: _description_
            project_configuration: _description_
            scm: _description_

        Returns:
            _description_
        """
        return resolve_pep621(pep621_configuration, project_configuration, scm)

    def _generate_core_data(
        self,
        project_data: ProjectData,
        local_configuration: CPPythonLocalConfiguration,
        plugin_cppython_date: PluginCPPythonData,
    ) -> CoreData:
        """Parses and returns resolved data from all configuration sources

        Args:
            project_data: Project data
            local_configuration: TODO
            plugin_cppython_date: TODO

        Raises:
            ConfigError: Raised if data cannot be parsed

        Returns:
            The resolved core object
        """

        global_configuration = CPPythonGlobalConfiguration()

        cppython_data = resolve_cppython(local_configuration, global_configuration, project_data, plugin_cppython_date)

        return CoreData(project_data=project_data, cppython_data=cppython_data)

    def _resolve_global_config(self) -> CPPythonGlobalConfiguration:
        """Generates the global configuration object

        Returns:
            The global configuration object
        """

        return CPPythonGlobalConfiguration()

    def _find_generators(self) -> list[type[Generator]]:
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
                    f"Found incompatible plugin. The '{loaded_type.name()}' plugin must be an instance of"
                    f" '{group_name}'"
                )
            else:
                self.logger.warning(f"{group_name} plugin found: {loaded_type.name()} from {getmodule(loaded_type)}")
                plugin_types.append(loaded_type)

        if not plugin_types:
            raise PluginError(f"No {group_name} plugin was found")

        return plugin_types

    def _find_providers(self) -> list[type[Provider]]:
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
                    f"Found incompatible plugin. The '{loaded_type.name()}' plugin must be an instance of"
                    f" '{group_name}'"
                )
            else:
                self.logger.warning(f"{group_name} plugin found: {loaded_type.name()} from {getmodule(loaded_type)}")
                plugin_types.append(loaded_type)

        if not plugin_types:
            raise PluginError(f"No {group_name} plugin was found")

        return plugin_types

    def _find_source_managers(self) -> list[type[SCM]]:
        """_summary_

        Raises:
            PluginError: _description_

        Returns:
            _description_
        """

        group_name = "scm"
        plugin_types: list[type[SCM]] = []

        # Filter entries by type
        for entry_point in list(metadata.entry_points(group=f"cppython.{group_name}")):
            loaded_type = entry_point.load()
            if not issubclass(loaded_type, SCM):
                self.logger.warning(
                    f"Found incompatible plugin. The '{loaded_type.name()}' plugin must be an instance of"
                    f" '{group_name}'"
                )
            else:
                self.logger.warning(f"{group_name} plugin found: {loaded_type.name()} from {getmodule(loaded_type)}")
                plugin_types.append(loaded_type)

        if not plugin_types:
            raise PluginError(f"No {group_name} plugin was found")

        return plugin_types

    def _filter_plugins[
        T: DataPlugin
    ](self, plugin_types: list[type[T]], pinned_name: str | None, group_name: str) -> list[type[T]]:
        """Finds and filters data plugins

        Args:
            plugin_types: The plugin type to lookup
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
                if loaded_type.name() == pinned_name:
                    self.logger.warning(
                        f"Using {group_name} plugin: {loaded_type.name()} from {getmodule(loaded_type)}"
                    )
                    return [loaded_type]

        self.logger.warning(f"'{group_name}_name' was empty. Trying to deduce {group_name}s")

        supported_types: list[type[T]] = []

        # Deduce types
        for loaded_type in plugin_types:
            self.logger.warning(
                f"A {group_name} plugin is supported: {loaded_type.name()} from {getmodule(loaded_type)}"
            )
            supported_types.append(loaded_type)

        # Fail
        if supported_types is None:
            raise PluginError(f"No {group_name} could be deduced from the root directory.")

        return supported_types

    def _select_scm(self, scm_plugins: list[type[SCM]], project_data: ProjectData) -> type[SCM]:
        """_summary_

        Args:
            scm_plugins: _description_
            project_data: _description_

        Raises:
            PluginError: _description_

        Returns:
            _description_
        """

        for scm_type in scm_plugins:
            if scm_type.features(project_data.pyproject_file.parent).repository:
                return scm_type

        raise PluginError("No SCM plugin was found that supports the given path")

    def _solve(
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

    def _create_scm(
        self,
        core_data: CoreData,
        scm_type: type[SCM],
    ) -> SCM:
        """_summary_

        Args:
            core_data: _description_
            scm_type: _description_

        Returns:
            _description_
        """

        cppython_plugin_data = resolve_cppython_plugin(core_data.cppython_data, scm_type)
        scm_data = resolve_scm(core_data.project_data, cppython_plugin_data)

        plugin = scm_type(scm_data)

        return plugin

    def _create_generator(
        self,
        core_data: CoreData,
        pep621_data: PEP621Data,
        generator_configuration: dict[str, Any],
        generator_type: type[Generator],
    ) -> Generator:
        """Creates a generator from input configuration

        Args:
            core_data: The resolved configuration data
            pep621_data: The PEP621 data
            generator_configuration: The generator table of the CPPython configuration data
            generator_type: The plugin type

        Returns:
            The constructed generator
        """

        cppython_plugin_data = resolve_cppython_plugin(core_data.cppython_data, generator_type)

        generator_data = resolve_generator(core_data.project_data, cppython_plugin_data)

        if not generator_configuration:
            self.logger.error(
                "The pyproject.toml table 'tool.cppython.generator' does not exist. Sending generator empty data",
            )

        core_plugin_data = CorePluginData(
            project_data=core_data.project_data,
            pep621_data=pep621_data,
            cppython_data=cppython_plugin_data,
        )

        return generator_type(generator_data, core_plugin_data, generator_configuration)

    def _create_provider(
        self,
        core_data: CoreData,
        pep621_data: PEP621Data,
        provider_configuration: dict[str, Any],
        provider_type: type[Provider],
    ) -> Provider:
        """Creates Providers from input data

        Args:
            core_data: The resolved configuration data
            pep621_data: The PEP621 data
            provider_configuration: The provider data table
            provider_type: The type to instantiate

        Returns:
            A constructed provider plugins
        """

        cppython_plugin_data = resolve_cppython_plugin(core_data.cppython_data, provider_type)

        provider_data = resolve_provider(core_data.project_data, cppython_plugin_data)

        if not provider_configuration:
            self.logger.error(
                "The pyproject.toml table 'tool.cppython.provider' does not exist. Sending provider empty data",
            )

        core_plugin_data = CorePluginData(
            project_data=core_data.project_data,
            pep621_data=pep621_data,
            cppython_data=cppython_plugin_data,
        )

        return provider_type(provider_data, core_plugin_data, provider_configuration)

    def build(self, pep621_configuration: PEP621Configuration, local_configuration: CPPythonLocalConfiguration) -> Data:
        """_summary_

        Args:
            pep621_configuration: _description_
            local_configuration: _description_

        Returns:
            _description_
        """

        project_data = resolve_project_configuration(self.project_configuration)

        plugin_build_data = self._generate_plugins(local_configuration, project_data)
        plugin_cppython_data = self._generate_cppython_plugin_data(plugin_build_data)

        core_data = self._generate_core_data(
            project_data,
            local_configuration,
            plugin_cppython_data,
        )

        scm = self._create_scm(core_data, plugin_build_data.scm_type)

        pep621_data = self._generate_pep621_data(pep621_configuration, self.project_configuration, scm)

        # Create the chosen plugins
        generator = self._create_generator(
            core_data, pep621_data, local_configuration.generator, plugin_build_data.generator_type
        )
        provider = self._create_provider(
            core_data, pep621_data, local_configuration.provider, plugin_build_data.provider_type
        )

        plugins = Plugins(generator=generator, provider=provider, scm=scm)

        return Data(core_data, plugins, self.logger)

"""Everything needed to build a CPPython project
"""

from collections.abc import Sequence
from importlib import metadata
from logging import Logger

from cppython_core.plugin_schema.provider import Provider
from cppython_core.plugin_schema.vcs import VersionControl
from cppython_core.schema import (
    CPPythonDataResolved,
    DataPlugin,
    PEP621Resolved,
    Plugin,
    PluginDataConfigurationT,
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

    def __init__(self, configuration: ProjectConfiguration, logger: Logger) -> None:
        self.configuration = configuration
        self.logger = logger

    def discover_providers(self) -> list[type[Provider]]:
        """Discovers plugin types
            TODO: With mypy 0.982+, disable abstract-type and make this generic for all plugins
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

    def discover_vcs(self) -> list[type[VersionControl]]:
        """Discovers plugin types
            TODO: With mypy 0.982+, disable abstract-type and make this generic for all plugins
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

    def create_data_plugins(
        self,
        plugins: Sequence[type[DataPlugin[PluginDataConfigurationT]]],
        configuration: PluginDataConfigurationT,
        project: PEP621Resolved,
        cppython: CPPythonDataResolved,
    ) -> list[DataPlugin[PluginDataConfigurationT]]:
        """Creates Providers from input data

        Args:
            plugins: List of plugins to construct
            configuration: Plugin configuration data
            project: Resolved project data
            cppython: Resolved cppython data

        Returns:
            List of constructed plugins
        """

        _providers = []
        for plugin_type in plugins:
            name = plugin_type.name()
            provider_data = getattr(cppython, name)
            resolved_provider_data = provider_data.resolve(configuration)
            resolved_cppython_data = cppython.resolve_plugin(plugin_type)

            _providers.append(plugin_type(configuration, project, resolved_cppython_data, resolved_provider_data))

        return _providers

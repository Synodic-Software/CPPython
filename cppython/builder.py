"""Everything needed to build a CPPython project
"""

from importlib import metadata
from logging import Logger
from pathlib import Path
from typing import Any

from cppython_core.schema import (
    ConfigurePreset,
    CPPythonData,
    CPPythonDataResolved,
    PEP621Resolved,
    Plugin,
    ProjectConfiguration,
    Provider,
    ProviderConfiguration,
    ProviderDataResolvedT,
    ProviderDataT,
    PyProject,
    ToolData,
)
from pydantic import create_model

from cppython.schema import CMakePresets
from cppython.utility import read_json, write_json, write_model_json


class PluginBuilder:
    """_summary_

    Returns:
        _description_
    """

    def __init__(self, group: str, logger: Logger) -> None:
        self._group = group
        self._logger = logger

    def gather_entries(self) -> list[metadata.EntryPoint]:
        """_summary_

        Returns:
            _description_
        """
        return list(metadata.entry_points(group=f"cppython.{self._group}"))

    def load(self, entry_points: list[metadata.EntryPoint]) -> list[type[Plugin]]:
        """_summary_

        Args:
            entry_points: _description_

        Raises:
            TypeError: _description_

        Returns:
            _description_
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

    def discover_providers(self) -> list[type[Provider[Any, Any]]]:
        """_summary_

        Raises:
            TypeError: _description_

        Returns:
            _description_
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

    def generate_model(self, plugins: list[type[Provider[ProviderDataT, ProviderDataResolvedT]]]) -> type[PyProject]:
        """_summary_

        Args:
            plugins: _description_

        Returns:
            _description_
        """
        plugin_fields: dict[str, Any] = {}
        for plugin_type in plugins:
            plugin_fields[plugin_type.name()] = (plugin_type.data_type(), ...)

        extended_cppython_type = create_model(
            "ExtendedCPPythonData",
            **plugin_fields,
            __base__=CPPythonData,
        )

        extended_tool_type = create_model(
            "ExtendedToolData",
            cppython=(extended_cppython_type, ...),
            __base__=ToolData,
        )

        return create_model(
            "ExtendedPyProject",
            tool=(extended_tool_type, ...),
            __base__=PyProject,
        )

    def generate_resolved_cppython_model(
        self, plugins: list[type[Provider[ProviderDataT, ProviderDataResolvedT]]]
    ) -> type[CPPythonDataResolved]:
        """_summary_

        Args:
            plugins: _description_

        Returns:
            _description_
        """

        plugin_fields: dict[str, Any] = {}
        for plugin_type in plugins:
            # The unresolved type is still appended to the CPPythonDataResolved type
            #   as sub-resolution still needs to happen at this stage of the builder
            plugin_fields[plugin_type.name()] = (plugin_type.data_type(), ...)

        return create_model(
            "ExtendedCPPythonDataResolved",
            **plugin_fields,
            __base__=CPPythonDataResolved,
        )

    def create_providers(
        self,
        plugins: list[type[Provider[ProviderDataT, ProviderDataResolvedT]]],
        project_configuration: ProjectConfiguration,
        configuration: ProviderConfiguration,
        static_resolved_project_data: tuple[PEP621Resolved, CPPythonDataResolved],
    ) -> list[Provider[ProviderDataT, ProviderDataResolvedT]]:
        """_summary_

        Args:
            plugins: _description_
            project_configuration: _description_
            configuration: _description_
            static_resolved_project_data: _description_

        Returns:
            _description_
        """

        project, cppython = static_resolved_project_data

        _providers = []
        for plugin_type in plugins:
            name = plugin_type.name()
            provider_data = getattr(cppython, name)
            resolved_provider_data = provider_data.resolve(project_configuration)
            resolved_cppython_data = cppython.provider_resolve(plugin_type)

            _providers.append(plugin_type(configuration, project, resolved_cppython_data, resolved_provider_data))

        return _providers

    def write_presets(self, path: Path, provider_output: list[tuple[str, ConfigurePreset]]) -> Path:
        """Write the cppython presets.

        Args:
            path: _description_
            provider_output: _description_

        Returns:
            _description_
        """

        path.mkdir(parents=True, exist_ok=True)

        def write_provider_presets(path: Path, provider_name: str, configure_preset: ConfigurePreset) -> Path:
            """Write a provider preset.

            Args:
                path: _description_
                provider_name: _description_
                configure_preset: _description_

            Returns:
                _description_
            """
            provider_tool_path = path / provider_name
            provider_tool_path.mkdir(parents=True, exist_ok=True)

            configure_preset.hidden = True
            presets = CMakePresets(configurePresets=[configure_preset])

            json_path = provider_tool_path / f"{provider_name}.json"

            write_model_json(json_path, presets)

            return json_path

        names = []
        includes = []

        path = path / "cppython"

        for provider_name, configure_preset in provider_output:
            preset_file = write_provider_presets(path, provider_name, configure_preset)

            relative_file = preset_file.relative_to(path)

            names.append(provider_name)
            includes.append(str(relative_file))

        configure_preset = ConfigurePreset(name="cppython", hidden=True, inherits=names)
        presets = CMakePresets(configurePresets=[configure_preset], include=includes)

        json_path = path / "cppython.json"

        write_model_json(json_path, presets)
        return json_path

    def write_root_presets(self, path: Path) -> None:
        """Read the top level json file and replace the include reference.
        Receives a relative path to the tool cmake json file

        Args:
            path: _description_
        """

        root_preset_path = self.configuration.pyproject_file.parent / "CMakePresets.json"

        root_preset = read_json(root_preset_path)
        root_model = CMakePresets.parse_obj(root_preset)

        if root_model.include is not None:
            for index, include_path in enumerate(root_model.include):
                if Path(include_path).name == "cppython.json":
                    root_model.include[index] = "build/" + path.as_posix()

            # 'dict.update' wont apply to nested types, manual replacement
            root_preset["include"] = root_model.include

            write_json(root_preset_path, root_preset)

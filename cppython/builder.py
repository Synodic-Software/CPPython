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
    Generator,
    GeneratorConfiguration,
    GeneratorDataResolvedT,
    GeneratorDataT,
    PEP621Resolved,
    Plugin,
    ProjectConfiguration,
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

    def discover_generators(self) -> list[type[Generator[Any, Any]]]:
        """_summary_

        Raises:
            TypeError: _description_

        Returns:
            _description_
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

    def generate_model(self, plugins: list[type[Generator[GeneratorDataT, GeneratorDataResolvedT]]]) -> type[PyProject]:
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
        self, plugins: list[type[Generator[GeneratorDataT, GeneratorDataResolvedT]]]
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

    def create_generators(
        self,
        plugins: list[type[Generator[GeneratorDataT, GeneratorDataResolvedT]]],
        project_configuration: ProjectConfiguration,
        configuration: GeneratorConfiguration,
        static_resolved_project_data: tuple[PEP621Resolved, CPPythonDataResolved],
    ) -> list[Generator[GeneratorDataT, GeneratorDataResolvedT]]:
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

        _generators = []
        for plugin_type in plugins:
            name = plugin_type.name()
            generator_data = getattr(cppython, name)
            resolved_generator_data = generator_data.resolve(project_configuration)
            resolved_cppython_data = cppython.generator_resolve(plugin_type)

            _generators.append(plugin_type(configuration, project, resolved_cppython_data, resolved_generator_data))

        return _generators

    def write_presets(self, path: Path, generator_output: list[tuple[str, ConfigurePreset]]) -> Path:
        """Write the cppython presets.

        Args:
            path: _description_
            generator_output: _description_

        Returns:
            _description_
        """

        path.mkdir(parents=True, exist_ok=True)

        def write_generator_presets(path: Path, generator_name: str, configure_preset: ConfigurePreset) -> Path:
            """Write a generator preset.

            Args:
                path: _description_
                generator_name: _description_
                configure_preset: _description_

            Returns:
                _description_
            """
            generator_tool_path = path / generator_name
            generator_tool_path.mkdir(parents=True, exist_ok=True)

            configure_preset.hidden = True
            presets = CMakePresets(configurePresets=[configure_preset])

            json_path = generator_tool_path / f"{generator_name}.json"

            write_model_json(json_path, presets)

            return json_path

        names = []
        includes = []

        path = path / "cppython"

        for generator_name, configure_preset in generator_output:
            preset_file = write_generator_presets(path, generator_name, configure_preset)

            relative_file = preset_file.relative_to(path)

            names.append(generator_name)
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

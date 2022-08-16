"""
TODO
"""

from importlib import metadata
from pathlib import Path
from typing import Type

from cppython_core.schema import (
    CPPythonData,
    CPPythonDataResolved,
    Generator,
    GeneratorConfiguration,
    PEP621Resolved,
    PluginT,
    ProjectConfiguration,
    PyProject,
    ToolData,
)
from pydantic import create_model

from cppython.schema import CMakePresets, ConfigurePreset
from cppython.utility import read_json, write_json, write_model_json


class Builder:
    """
    TODO
    """

    def __init__(self, configuration: ProjectConfiguration) -> None:
        self.configuration = configuration

    def gather_plugins(self, plugin_type: Type[PluginT]) -> list[Type[PluginT]]:
        """
        TODO
        """
        plugins = []
        entry_points = metadata.entry_points(group=f"cppython.{plugin_type.group()}")

        for entry_point in entry_points:
            loaded_plugin_type = entry_point.load()
            if issubclass(loaded_plugin_type, plugin_type) & (loaded_plugin_type is not plugin_type):
                plugins.append(loaded_plugin_type)

        return plugins

    def generate_model(self, plugins: list[Type[Generator]]) -> Type[PyProject]:
        """
        TODO: Proper return type hint
        """
        plugin_fields = {}
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

    def generate_resolved_cppython_model(self, plugins: list[Type[Generator]]) -> Type[CPPythonDataResolved]:
        """
        TODO
        """

        plugin_fields = {}
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
        plugins: list[Type[Generator]],
        project_configuration: ProjectConfiguration,
        configuration: GeneratorConfiguration,
        project: PEP621Resolved,
        cppython: CPPythonDataResolved,
    ) -> list[Generator]:
        """
        TODO
        """
        _generators = []
        for plugin_type in plugins:
            name = plugin_type.name()
            generator_data = getattr(cppython, name)
            resolved_generator_data = generator_data.resolve(project_configuration)
            _generators.append(plugin_type(configuration, project, cppython, resolved_generator_data))

        return _generators

    def write_presets(self, path: Path, generator_output: list[tuple[str, ConfigurePreset]]) -> Path:
        """
        Write the cppython presets.
        Returns the
        """

        path.mkdir(parents=True, exist_ok=True)

        def write_generator_presets(path: Path, generator_name: str, configure_preset: ConfigurePreset) -> Path:
            """
            Write a generator preset.
            @returns - The written json file
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

    def write_root_presets(self, path: Path):
        """
        Read the top level json file and replace the include reference.
        Receives a relative path to the tool cmake json file
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

"""
The central delegation of the CPPython project
"""

import logging
from importlib import metadata
from pathlib import Path
from typing import Any, Type, TypeVar

from cppython_core.schema import (
    PEP621,
    CPPythonData,
    CPPythonDataT,
    Generator,
    GeneratorConfiguration,
    Interface,
    Plugin,
    ProjectDataT,
    PyProject,
    ToolData,
)
from cppython_core.utility import cppython_logger
from pydantic import create_model

from cppython.schema import API, CMakePresets, ConfigurePreset, ProjectConfiguration
from cppython.utility import read_json, write_json, write_model_json


class ProjectBuilder:
    """
    TODO
    """

    def __init__(self, configuration: ProjectConfiguration) -> None:
        self.configuration = configuration

    DerivedPlugin = TypeVar("DerivedPlugin", bound=Plugin)

    def gather_plugins(self, plugin_type: Type[DerivedPlugin]) -> list[Type[DerivedPlugin]]:
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

    def create_generators(
        self,
        plugins: list[Type[Generator]],
        configuration: GeneratorConfiguration,
        project: PEP621,
        cppython: CPPythonData,
    ) -> list[Generator]:
        """
        TODO
        """
        _generators = []
        for plugin_type in plugins:
            name = plugin_type.name()
            _generators.append(plugin_type(configuration, project, cppython, getattr(cppython, name)))

        return _generators

    def generate_modified_project(self, original: ProjectDataT) -> ProjectDataT:
        """
        Applies dynamic behaviors of the settings to itself
        Returns a copy of the original with dynamic modifications
        """
        modified = original.copy(deep=True)

        # Update the dynamic version

        modified.version = self.configuration.version

        return modified

    def generate_modified_cppython(self, original: CPPythonDataT) -> CPPythonDataT:
        """
        Applies dynamic behaviors of the settings to itself
        Returns a copy of the original with dynamic modifications
        """
        modified = original.copy(deep=True)

        # Add the pyproject.toml location to all relative paths

        if not modified.install_path.is_absolute():
            modified.install_path = self.configuration.root_path.absolute() / modified.install_path

        if not modified.tool_path.is_absolute():
            modified.tool_path = self.configuration.root_path.absolute() / modified.tool_path

        if not modified.build_path.is_absolute():
            modified.build_path = self.configuration.root_path.absolute() / modified.build_path

        return modified

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

        root_preset_path = self.configuration.root_path / "CMakePresets.json"

        root_preset = read_json(root_preset_path)
        root_model = CMakePresets.parse_obj(root_preset)

        if root_model.include is not None:
            for index, include_path in enumerate(root_model.include):
                if Path(include_path).name == "cppython.json":
                    root_model.include[index] = "build/" + path.as_posix()

            # 'dict.update' wont apply to nested types, manual replacement
            root_preset["include"] = root_model.include

            write_json(root_preset_path, root_preset)


class Project(API):
    """
    The object constructed at each entry_point
    """

    def __init__(
        self, configuration: ProjectConfiguration, interface: Interface, pyproject_data: dict[str, Any]
    ) -> None:

        self._enabled = False
        self._configuration = configuration

        levels = [logging.WARNING, logging.INFO, logging.DEBUG]

        # Add default output stream
        console_handler = logging.StreamHandler()
        cppython_logger.addHandler(console_handler)
        cppython_logger.setLevel(levels[configuration.verbosity])

        cppython_logger.info("Initializing project")

        self._builder = ProjectBuilder(self.configuration)
        plugins = self._builder.gather_plugins(Generator)

        if not plugins:
            cppython_logger.error("No generator plugin was found")
            return

        for plugin in plugins:
            cppython_logger.warning(f"Generator plugin found: {plugin.name()}")

        extended_pyproject_type = self._builder.generate_model(plugins)
        pyproject = extended_pyproject_type(**pyproject_data)

        if pyproject is None:
            cppython_logger.error("Data is not defined")
            return

        if pyproject.tool is None:
            cppython_logger.error("Table [tool] is not defined")
            return

        if pyproject.tool.cppython is None:
            cppython_logger.error("Table [tool.cppython] is not defined")
            return

        self._enabled = True

        self._project = pyproject.project

        self._modified_project_data = self._builder.generate_modified_project(pyproject.project)
        self._modified_cppython_data = self._builder.generate_modified_cppython(pyproject.tool.cppython)

        self._interface = interface

        generator_configuration = GeneratorConfiguration(root_path=self.configuration.root_path)
        self._generators = self._builder.create_generators(
            plugins, generator_configuration, self.project, self.cppython
        )

        cppython_logger.info("Initialized project successfully")

    @property
    def enabled(self) -> bool:
        """
        TODO
        """
        return self._enabled

    @property
    def configuration(self) -> ProjectConfiguration:
        """
        TODO
        """
        return self._configuration

    @property
    def project(self) -> PEP621:
        """
        The resolved pyproject project table
        """
        return self._modified_project_data

    @property
    def cppython(self):
        """
        The resolved CPPython data
        """
        return self._modified_cppython_data

    def download_generator_tools(self) -> None:
        """
        Download the generator tooling if required
        """
        if not self._enabled:
            cppython_logger.info("Skipping 'download_generator_tools' because the project is not enabled")
            return

        base_path = self.cppython.install_path

        for generator in self._generators:

            path = base_path / generator.name()

            path.mkdir(parents=True, exist_ok=True)

            if not generator.generator_downloaded(path):
                cppython_logger.warning(f"Downloading the {generator.name()} requirements to {path}")

                # TODO: Make async with progress bar
                generator.download_generator(path)
                cppython_logger.warning("Download complete")
            else:
                cppython_logger.info(f"The {generator.name()} generator is already downloaded")

    def update_generator_tools(self) -> None:
        """
        Update the generator tooling if available
        """
        if not self._enabled:
            cppython_logger.info("Skipping 'update_generator_tools' because the project is not enabled")
            return

        self.download_generator_tools()

        base_path = self.cppython.install_path

        for generator in self._generators:

            path = base_path / generator.name()

            generator.update_generator(path)

    # API Contract
    def install(self) -> None:
        """
        TODO
        """
        if not self._enabled:
            cppython_logger.info("Skipping install because the project is not enabled")
            return

        cppython_logger.info("Installing tools")
        self.download_generator_tools()

        cppython_logger.info("Installing project")
        preset_path = self.cppython.build_path

        generator_output = []

        # TODO: Async
        for generator in self._generators:
            cppython_logger.info(f"Installing {generator.name()} generator")

            try:
                generator.install()
                config_preset = generator.generate_cmake_config()
                generator_output.append((generator.name(), config_preset))
            except Exception as exception:
                cppython_logger.error(f"Generator {generator.name()} failed to install")
                raise exception

        project_presets = self._builder.write_presets(preset_path, generator_output)
        self._builder.write_root_presets(project_presets.relative_to(preset_path))

    def update(self) -> None:
        """
        TODO
        """
        if not self._enabled:
            cppython_logger.info("Skipping update because the project is not enabled")
            return

        cppython_logger.info("Updating tools")
        self.update_generator_tools()

        cppython_logger.info("Updating project")

        preset_path = self.cppython.build_path

        generator_output = []

        # TODO: Async
        for generator in self._generators:
            cppython_logger.info(f"Updating {generator.name()} generator")

            try:
                generator.update()
                config_preset = generator.generate_cmake_config()
                generator_output.append((generator.name(), config_preset))
            except Exception as exception:
                cppython_logger.error(f"Generator {generator.name()} failed to update")
                raise exception

        project_presets = self._builder.write_presets(preset_path, generator_output)
        self._builder.write_root_presets(project_presets.relative_to(preset_path))

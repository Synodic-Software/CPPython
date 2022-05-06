"""
The central delegation of the CPPython project
"""

import logging
from dataclasses import dataclass
from importlib import metadata
from typing import Any, Type, TypeVar

from cppython_core.core import cppython_logger
from cppython_core.schema import (
    API,
    CPPythonData,
    Generator,
    GeneratorConfiguration,
    Interface,
    Plugin,
    PyProject,
    ToolData,
)
from pydantic import create_model


@dataclass
class ProjectConfiguration:
    """
    TODO
    """

    _verbosity: int = 0

    @property
    def verbosity(self) -> int:
        """
        TODO
        """
        return self._verbosity

    @verbosity.setter
    def verbosity(self, value: int) -> None:
        """
        TODO
        """
        self._verbosity = min(max(value, 0), 2)


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
        self, plugins: list[Type[Generator]], configuration: GeneratorConfiguration, pyproject: PyProject
    ) -> list[Generator]:
        """
        TODO
        """
        _generators = []
        for plugin_type in plugins:
            _generators.append(plugin_type(configuration, pyproject))

        return _generators


class Project(API):
    """
    The object constructed at each entry_point
    """

    def __init__(
        self, configuration: ProjectConfiguration, interface: Interface, pyproject_data: dict[str, Any]
    ) -> None:

        self._enabled = False
        self._configuration = configuration
        self._pyproject = None

        levels = [logging.WARNING, logging.INFO, logging.DEBUG]

        # Add default output stream
        console_handler = logging.StreamHandler()
        cppython_logger.addHandler(console_handler)
        cppython_logger.setLevel(levels[configuration.verbosity])

        cppython_logger.info("Initializing project")

        builder = ProjectBuilder(self.configuration)
        plugins = builder.gather_plugins(Generator)

        if not plugins:
            cppython_logger.error("No generator plugin was found")
            return

        for plugin in plugins:
            cppython_logger.warning(f"Generator plugin found: {plugin.name()}")

        extended_pyproject_type = builder.generate_model(plugins)
        self._pyproject = extended_pyproject_type(**pyproject_data)

        if self.pyproject is None:
            cppython_logger.error("Data is not defined")
            return

        if self.pyproject.tool is None:
            cppython_logger.error("Table [tool] is not defined")
            return

        if self.pyproject.tool.cppython is None:
            cppython_logger.error("Table [tool.cppython] is not defined")
            return

        self._enabled = True

        self._interface = interface

        generator_configuration = GeneratorConfiguration()
        self._generators = builder.create_generators(plugins, generator_configuration, self.pyproject)

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
    def pyproject(self) -> PyProject | None:
        """
        TODO
        """
        return self._pyproject

    def download(self):
        """
        Download the generator tooling if required
        """
        if self._enabled:
            base_path = self.pyproject.tool.cppython.install_path

            for generator in self._generators:

                path = base_path / generator.name()

                path.mkdir(parents=True, exist_ok=True)

                if not generator.generator_downloaded(path):
                    cppython_logger.warning(f"Downloading the {generator.name()} requirements to {path}")

                    # TODO: Make async with progress bar
                    generator.download_generator(path)
                    cppython_logger.warning("Download complete")

    # API Contract

    def install(self) -> None:
        if self._enabled:
            cppython_logger.info("Installing project")
            self.download()

            for generator in self._generators:
                cppython_logger.info(f"Installing {generator.name()} generator")
                generator.install()

    def update(self) -> None:
        if self._enabled:
            cppython_logger.info("Updating project")

            for generator in self._generators:
                cppython_logger.info(f"Updating {generator.name()} generator")
                generator.update()

    def build(self) -> None:
        if self._enabled:
            cppython_logger.info("Building project")

            for generator in self._generators:
                cppython_logger.info(f"Building {generator.name()} generator")
                generator.build()

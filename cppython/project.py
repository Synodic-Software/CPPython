"""Manages data flow to and from plugins
"""

import asyncio
import logging
from typing import Any

from cppython_core.schema import (
    CPPythonDataResolved,
    Generator,
    GeneratorConfiguration,
    Interface,
    PEP621Resolved,
    ProjectConfiguration,
)

from cppython.builder import Builder
from cppython.schema import API


class Project(API):
    """The object constructed at each entry_point"""

    def __init__(
        self, configuration: ProjectConfiguration, interface: Interface, pyproject_data: dict[str, Any]
    ) -> None:
        self._enabled = False
        self._configuration = configuration

        levels = [logging.WARNING, logging.INFO, logging.DEBUG]

        # Add default output stream
        console_handler = logging.StreamHandler()
        self.logger = logging.getLogger("cppython")
        self.logger.addHandler(console_handler)
        self.logger.setLevel(levels[configuration.verbosity])

        self.logger.info("Initializing project")

        self._builder = Builder(self.configuration)

        if not (plugins := self._builder.gather_plugins(Generator)):
            self.logger.error("No generator plugin was found")
            return

        for plugin in plugins:
            self.logger.warning("Generator plugin found: %s", plugin.name())

        extended_pyproject_type = self._builder.generate_model(plugins)

        if (pyproject := extended_pyproject_type(**pyproject_data)) is None:
            self.logger.error("Data is not defined")
            return

        if pyproject.tool is None:
            self.logger.error("Table [tool] is not defined")
            return

        if pyproject.tool.cppython is None:
            self.logger.error("Table [tool.cppython] is not defined")
            return

        self._enabled = True

        self._project = pyproject.project

        resolved_cppython_model = self._builder.generate_resolved_cppython_model(plugins)
        self._resolved_project_data = pyproject.project.resolve(self.configuration)
        self._resolved_cppython_data = pyproject.tool.cppython.resolve(resolved_cppython_model, self.configuration)

        self._interface = interface

        generator_configuration = GeneratorConfiguration(root_directory=self.configuration.pyproject_file.parent)
        self._generators = self._builder.create_generators(
            plugins, self.configuration, generator_configuration, (self.project, self.cppython)
        )

        self.logger.info("Initialized project successfully")

    @property
    def enabled(self) -> bool:
        """_summary_

        Returns:
            _description_
        """
        return self._enabled

    @property
    def configuration(self) -> ProjectConfiguration:
        """_summary_

        Returns:
            _description_
        """
        return self._configuration

    @property
    def project(self) -> PEP621Resolved:
        """_summary_

        Returns:
            _description_
        """
        return self._resolved_project_data

    @property
    def cppython(self) -> CPPythonDataResolved:
        """The resolved CPPython data

        Returns:
            _description_
        """
        return self._resolved_cppython_data

    async def download_generator_tools(self) -> None:
        """Download the generator tooling if required"""
        if not self._enabled:
            self.logger.info("Skipping 'download_generator_tools' because the project is not enabled")
            return

        base_path = self.cppython.install_path

        for generator in self._generators:
            path = base_path / generator.name()

            path.mkdir(parents=True, exist_ok=True)

            if not generator.tooling_downloaded(path):
                self.logger.warning("Downloading the %s requirements to %s", generator.name(), path)

                # TODO: Make async with progress bar
                await generator.download_tooling(path)
                self.logger.warning("Download complete")
            else:
                self.logger.info("The %s generator is already downloaded", generator.name())

    # API Contract
    def install(self) -> None:
        """_summary_

        Raises:
            Exception: _description_
        """
        if not self._enabled:
            self.logger.info("Skipping install because the project is not enabled")
            return

        self.logger.info("Installing tools")
        asyncio.run(self.download_generator_tools())

        self.logger.info("Installing project")
        preset_path = self.cppython.build_path

        generator_output = []

        # TODO: Async
        for generator in self._generators:
            self.logger.info("Installing %s generator", generator.name())

            try:
                generator.install()
                config_preset = generator.generate_cmake_config()
                generator_output.append((generator.name(), config_preset))
            except Exception as exception:
                self.logger.error("Generator %s failed to install", generator.name())
                raise exception

        project_presets = self._builder.write_presets(preset_path, generator_output)
        self._builder.write_root_presets(project_presets.relative_to(preset_path))

    def update(self) -> None:
        """_summary_

        Raises:
            Exception: _description_
        """
        if not self._enabled:
            self.logger.info("Skipping update because the project is not enabled")
            return

        self.logger.info("Updating tools")
        asyncio.run(self.download_generator_tools())

        self.logger.info("Updating project")

        preset_path = self.cppython.build_path

        generator_output = []

        # TODO: Async
        for generator in self._generators:
            self.logger.info("Updating %s generator", generator.name())

            try:
                generator.update()
                config_preset = generator.generate_cmake_config()
                generator_output.append((generator.name(), config_preset))
            except Exception as exception:
                self.logger.error("Generator %s failed to update", generator.name())
                raise exception

        project_presets = self._builder.write_presets(preset_path, generator_output)
        self._builder.write_root_presets(project_presets.relative_to(preset_path))

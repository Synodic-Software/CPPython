"""Manages data flow to and from plugins
"""

import asyncio
import logging
from typing import Any

from cppython_core.exceptions import ConfigError, PluginError
from cppython_core.plugin_schema.interface import Interface
from cppython_core.schema import CoreData, ProjectConfiguration, PyProject

from cppython.builder import Builder
from cppython.schema import API


class Project(API):
    """The object constructed at each entry_point"""

    def __init__(
        self, configuration: ProjectConfiguration, interface: Interface, pyproject_data: dict[str, Any]
    ) -> None:
        self._enabled = False
        self._interface = interface

        # Default logging levels
        levels = [logging.WARNING, logging.INFO, logging.DEBUG]

        # Add default output stream
        self.logger = logging.getLogger("cppython")
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(levels[configuration.verbosity])

        self.logger.info("Initializing project")

        if (pyproject := PyProject(**pyproject_data)) is None:
            raise ConfigError("PyProject data is not defined")

        builder = Builder(self.logger)

        if not (provider_plugins := builder.discover_providers()):
            raise PluginError("No provider plugin was found")

        for provider_plugin in provider_plugins:
            self.logger.warning("Provider plugin found: %s", provider_plugin.name())

        if not (generator_plugins := builder.discover_generators()):
            raise PluginError("No generator plugin was found")

        for generator_plugin in generator_plugins:
            self.logger.warning("Generator plugin found: %s", generator_plugin.name())

        if pyproject.tool is None:
            raise ConfigError("Table [tool] is not defined")

        if pyproject.tool.cppython is None:
            raise ConfigError("Table [tool.cppython] is not defined")

        self._core_data = builder.generate_core_data(configuration, pyproject.project, pyproject.tool.cppython)

        self._providers = builder.create_providers(provider_plugins, self.core_data, pyproject.tool.cppython.provider)
        self._generator = builder.create_generator(generator_plugins, self.core_data, pyproject.tool.cppython.generator)

        self._enabled = True

        self.logger.info("Initialized project successfully")

    @property
    def enabled(self) -> bool:
        """Queries if the project was is initialized for full functionality

        Returns:
            The query result
        """
        return self._enabled

    @property
    def core_data(self) -> CoreData:
        """Queries if the project was is initialized for full functionality

        Returns:
            The query result
        """
        return self._core_data

    async def download_provider_tools(self) -> None:
        """Download the provider tooling if required"""
        if not self._enabled:
            self.logger.info("Skipping 'download_provider_tools' because the project is not enabled")
            return

        base_path = self.core_data.cppython_data.install_path

        for provider in self._providers:
            path = base_path / provider.name()

            path.mkdir(parents=True, exist_ok=True)

            if not provider.tooling_downloaded(path):
                self.logger.warning("Downloading the %s requirements to %s", provider.name(), path)

                await provider.download_tooling(path)
                self.logger.warning("Download complete")
            else:
                self.logger.info("The %s provider is already downloaded", provider.name())

    # API Contract
    def install(self) -> None:
        """Installs project dependencies

        Raises:
            Exception: Raised if failed
        """
        if not self._enabled:
            self.logger.info("Skipping install because the project is not enabled")
            return

        self.logger.info("Installing tools")
        asyncio.run(self.download_provider_tools())

        self.logger.info("Installing project")

        for provider in self._providers:
            self.logger.info("Installing %s provider", provider.name())

            try:
                provider.install()
            except Exception as exception:
                self.logger.error("Provider %s failed to install", provider.name())
                raise exception

    def update(self) -> None:
        """Updates project dependencies

        Raises:
            Exception: Raised if failed
        """
        if not self._enabled:
            self.logger.info("Skipping update because the project is not enabled")
            return

        self.logger.info("Updating tools")
        asyncio.run(self.download_provider_tools())

        self.logger.info("Updating project")

        for provider in self._providers:
            self.logger.info("Updating %s provider", provider.name())

            try:
                provider.update()
            except Exception as exception:
                self.logger.error("Provider %s failed to update", provider.name())
                raise exception

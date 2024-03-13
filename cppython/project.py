"""Manages data flow to and from plugins"""

import asyncio
import logging
from typing import Any

from cppython_core.exceptions import ConfigException, PluginError
from cppython_core.resolution import resolve_model
from cppython_core.schema import CoreData, Interface, ProjectConfiguration, PyProject

from cppython.builder import Builder
from cppython.schema import API


class Project(API):
    """The object that should be constructed at each entry_point"""

    def __init__(
        self, project_configuration: ProjectConfiguration, interface: Interface, pyproject_data: dict[str, Any]
    ) -> None:
        self._enabled = False
        self._interface = interface
        self.logger = logging.getLogger("cppython")

        builder = Builder(project_configuration, self.logger)

        self.logger.info("Initializing project")

        try:
            pyproject = resolve_model(PyProject, pyproject_data)
        except ConfigException as error:
            self.logger.error(error, exc_info=True)
            return

        if not pyproject.tool or not pyproject.tool.cppython:
            self.logger.warning("The pyproject.toml file doesn't contain the `tool.cppython` table")
            return

        self._plugins = builder.build(pyproject.project, pyproject.tool.cppython)

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
    def core_data(self) -> CoreData | None:
        """Core data

        Returns:
            Core data, if enabled
        """
        return self._core_data if self._enabled else None

    async def download_provider_tools(self) -> None:
        """Download the provider tooling if required"""
        if not self._enabled:
            self.logger.info("Skipping 'download_provider_tools' because the project is not enabled")
            return

        base_path = self._core_data.cppython_data.install_path

        path = base_path / self._provider.name()

        path.mkdir(parents=True, exist_ok=True)

        self.logger.warning("Downloading the %s requirements to %s", self._provider.name(), path)
        await self._provider.download_tooling(path)

    def sync(self) -> None:
        """Gathers sync information from providers and passes it to the generator

        Raises:
            PluginError: Plugin error
        """

        if (sync_data := self._provider.sync_data(self._generator)) is None:
            raise PluginError("The provider doesn't support the generator")

        self._generator.sync(sync_data)

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
        self.logger.info("Installing %s provider", self._provider.name())

        try:
            self._provider.install()
        except Exception as exception:
            self.logger.error("Provider %s failed to install", self._provider.name())
            raise exception

        self.sync()

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
        self.logger.info("Updating %s provider", self._provider.name())

        try:
            self._provider.update()
        except Exception as exception:
            self.logger.error("Provider %s failed to update", self._provider.name())
            raise exception

        self.sync()

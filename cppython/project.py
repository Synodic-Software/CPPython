"""Manages data flow to and from plugins
"""

import asyncio
import logging
from typing import Any

from cppython_core.plugin_schema.interface import Interface
from cppython_core.resolution import (
    resolve_cppython,
    resolve_pep621,
    resolve_project_configuration,
)
from cppython_core.schema import (
    CPPythonData,
    CPPythonGlobalConfiguration,
    PEP621Data,
    ProjectConfiguration,
    PyProject,
)

from cppython.builder import Builder
from cppython.schema import API


class Project(API):
    """The object constructed at each entry_point"""

    def __init__(
        self, configuration: ProjectConfiguration, interface: Interface, pyproject_data: dict[str, Any]
    ) -> None:
        self._enabled = False

        # Default logging levels
        levels = [logging.WARNING, logging.INFO, logging.DEBUG]

        # Add default output stream
        self.logger = logging.getLogger("cppython")
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(levels[configuration.verbosity])

        self.logger.info("Initializing project")

        builder = Builder(self.logger)

        if not (plugins := builder.discover_providers()):
            self.logger.error("No provider plugin was found")
            return

        for plugin in plugins:
            self.logger.warning("Provider plugin found: %s", plugin.name())

        if (pyproject := PyProject(**pyproject_data)) is None:
            self.logger.error("Data is not defined")
            return

        if pyproject.tool is None:
            self.logger.error("Table [tool] is not defined")
            return

        if pyproject.tool.cppython is None:
            self.logger.error("Table [tool.cppython] is not defined")
            return

        self._enabled = True

        project_data = resolve_project_configuration(configuration)
        self._resolved_pep621_data = resolve_pep621(pyproject.project, configuration)
        self._resolved_cppython_data = resolve_cppython(
            pyproject.tool.cppython, CPPythonGlobalConfiguration(), project_data
        )

        self._interface = interface

        self._providers = builder.create_providers(
            plugins, project_data, self.pep621_data, pyproject.tool.cppython, self.cppython_data
        )

        self.logger.info("Initialized project successfully")

    @property
    def enabled(self) -> bool:
        """Queries if the project was is initialized for full functionality

        Returns:
            The query result
        """
        return self._enabled

    @property
    def pep621_data(self) -> PEP621Data:
        """Resolved project data

        Returns:
            The resolved 'project' table
        """
        return self._resolved_pep621_data

    @property
    def cppython_data(self) -> CPPythonData:
        """The resolved CPPython data

        Returns:
            Resolved 'cppython' table
        """
        return self._resolved_cppython_data

    async def download_provider_tools(self) -> None:
        """Download the provider tooling if required"""
        if not self._enabled:
            self.logger.info("Skipping 'download_provider_tools' because the project is not enabled")
            return

        base_path = self.cppython_data.install_path

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

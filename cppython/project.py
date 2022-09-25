"""Manages data flow to and from plugins
"""

import asyncio
import logging
from typing import Any

from cppython_core.schema import (
    CPPythonDataResolved,
    Interface,
    PEP621Resolved,
    ProjectConfiguration,
    ProviderConfiguration,
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

        builder = Builder(configuration, self.logger)

        if not (plugins := builder.discover_providers()):
            self.logger.error("No provider plugin was found")
            return

        for plugin in plugins:
            self.logger.warning("Provider plugin found: %s", plugin.name())

        extended_pyproject_type = builder.generate_model(plugins)

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

        resolved_cppython_model = builder.generate_resolved_cppython_model(plugins)
        self._resolved_project_data = pyproject.project.resolve(configuration)
        self._resolved_cppython_data = pyproject.tool.cppython.resolve(resolved_cppython_model, configuration)

        self._interface = interface

        provider_configuration = ProviderConfiguration(root_directory=configuration.pyproject_file.parent)
        self._providers = builder.create_providers(
            plugins, configuration, provider_configuration, (self.project, self.cppython)
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
    def project(self) -> PEP621Resolved:
        """Resolved project data

        Returns:
            The resolved 'project' table
        """
        return self._resolved_project_data

    @property
    def cppython(self) -> CPPythonDataResolved:
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

        base_path = self.cppython.install_path

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

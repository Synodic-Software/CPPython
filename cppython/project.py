"""Manages data flow to and from plugins
"""

import asyncio
import logging
from typing import Any

from cppython_core.exceptions import ConfigError, PluginError
from cppython_core.plugin_schema.scm import SCM
from cppython_core.resolution import resolve_name
from cppython_core.schema import CoreData, Interface, ProjectConfiguration, PyProject
from pydantic import ValidationError

from cppython.builder import Builder
from cppython.schema import API


class Project(API):
    """The object constructed at each entry_point"""

    def __init__(
        self, project_configuration: ProjectConfiguration, interface: Interface, pyproject_data: dict[str, Any]
    ) -> None:
        self._enabled = False
        self._interface = interface
        self.logger = logging.getLogger("cppython")

        try:
            builder = Builder(self.logger)
            builder.setup_logger(project_configuration)

            self.logger.info("Initializing project")

            project_data = builder.generate_project_data(project_configuration)
            pyproject = PyProject(**pyproject_data)

            plugin_build_data = builder.generate_plugins(pyproject)

            # Once the plugins are resolved, the core data is complete and can be generated
            self.scm = plugin_build_data.scm_type()

            pep621_data = builder.generate_pep621_data(pyproject, project_configuration, self.scm)
            self._core_data = builder.generate_core_data(
                project_data,
                pyproject,
                plugin_build_data,
            )

            # Create the chosen plugins
            self._generator = builder.create_generator(
                self._core_data, pyproject.tool.cppython.generator, plugin_build_data.generator_type
            )
            self._provider = builder.create_provider(
                self._core_data, pyproject.tool.cppython.provider, plugin_build_data.provider_type
            )

        except ConfigError:
            logging.exception("Unhandled configuration. CPPython will process no further")
            return
        except ValidationError as error:
            logging.error(error)
            return

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

    @property
    def scm(self) -> SCM | None:
        """SCM

        Returns:
            SCM, if enabled
        """
        return self._scm if self._enabled else None

    async def download_provider_tools(self) -> None:
        """Download the provider tooling if required"""
        if not self._enabled:
            self.logger.info("Skipping 'download_provider_tools' because the project is not enabled")
            return

        name = resolve_name(type(self._provider))
        base_path = self._core_data.cppython_data.install_path

        path = base_path / name

        path.mkdir(parents=True, exist_ok=True)

        self.logger.warning("Downloading the %s requirements to %s", name, path)
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
        name = resolve_name(type(self._provider))
        self.logger.info("Installing %s provider", name)

        try:
            self._provider.install()
        except Exception as exception:
            self.logger.error("Provider %s failed to install", name)
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
        name = resolve_name(type(self._provider))
        self.logger.info("Updating %s provider", name)

        try:
            self._provider.update()
        except Exception as exception:
            self.logger.error("Provider %s failed to update", name)
            raise exception

        self.sync()

# Plugin
from cleo.events.console_events import COMMAND
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.plugins.application_plugin import ApplicationPlugin

# Commands
from poetry.console.commands.install import InstallCommand
from poetry.console.commands.update import UpdateCommand
from poetry.console.commands.check import CheckCommand

# CPPoetry
from cppoetry.utility import Metadata
from cppoetry.core import CPPoetryAPI

class SynodicPlugin(ApplicationPlugin):
    def __init__(self):
       pass

    def __del__(self):
        """
        Saves the project file if there have been any writes
        """

        if self._metadata.dirty:
            self._project.save()

    def _command_dispatch(
        self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher
    ) -> None:
        command = event.command

        # TODO: Condense
        if isinstance(command, InstallCommand):
            self.install()
        if isinstance(command, UpdateCommand):
            self.update()
        if isinstance(command, CheckCommand):
           self. check()

    def activate(self, application: Application):
        """
        The entry function for the Poetry plugin
        """

        self._project = application.poetry.pyproject
        self._metadata = Metadata(self._project.file, self._project.data)

        application.event_dispatcher.add_listener(COMMAND, self._command_dispatch)

    def install(self) -> None:

        CPPoetryAPI(self._project.file, self._metadata).install()

    def update(self) -> None:

        CPPoetryAPI(self._project.file, self._metadata).update()

    def check(self) -> None:

        CPPoetryAPI(self._project.file, self._metadata).validate()
# Plugin
from cleo.events.console_events import COMMAND
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.poetry import Poetry

# Document
from pathlib import Path
from poetry.core.pyproject.toml import PyProjectTOML
from cppoetry.utility import Metadata


class SynodicPlugin(ApplicationPlugin):
    def __init__(self):
        """
        Extracts the plugin database from the existing Poetry data
        """

        # TODO: Project location management
        self.project = PyProjectTOML("pyproject.toml")
        self.metadata = Metadata(self.project.data)

    def __del__(self):
        """
        Saves the project file if there have been any writes
        """

        if self.metadata.dirty:
            self.project.save()

    def activate(self, application: Application):
        """
        The entry function for the Poetry plugin
        """

        # application.event_dispatcher.add_listener(COMMAND, self.new)

    def install(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def update(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def check(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass
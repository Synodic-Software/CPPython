import toml

from pathlib import Path

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

# CPPython
from cppython.data import Metadata
from cppython.core import CPPythonAPI


class SynodicPlugin(ApplicationPlugin):
    def __init__(self):

        self._available_commands = {
            InstallCommand: self._install,
            UpdateCommand: self._update,
            CheckCommand: self._check,
        }

    def _command_dispatch(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:
        command = event.command

        # TODO: Use internally
        io = event.io
        if io.is_debug():
            io.write_line("<debug>Running plugin command setup.</debug>")

        if command in self._available_commands:
            self._available_commands[command](command)

    def activate(self, application: Application):
        """
        The entry function for the Poetry plugin
        """
        # pyproject will only be used for writing. tomlkit virally adds metadata
        self._project = application.poetry.pyproject

        data = toml.load(Path.cwd() / "pyproject.toml")

        self._metadata = Metadata(data['tool']['conan'])

        application.event_dispatcher.add_listener(COMMAND, self._command_dispatch)

        self.api = CPPythonAPI(self._project.file, self._metadata)

    def _install(self, command: InstallCommand) -> None:

        self.api.install()

    def _update(self, command: UpdateCommand) -> None:

        self.api.update()

    def _check(self, command: CheckCommand) -> None:

        self.api.validate()

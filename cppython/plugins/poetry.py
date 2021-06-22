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
from cppython.core import PEP621, Project, Plugin
from cppython.api import CPPythonAPI


class CPPythonPlugin(ApplicationPlugin):
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
        self._data = application.poetry.pyproject.data
        self._project = Project(application.poetry.file, self._data)

        application.event_dispatcher.add_listener(COMMAND, self._command_dispatch)

        self._api = CPPythonAPI(application.poetry.pyproject.file, self._project)

    def _install(self, command: InstallCommand) -> None:
        pass
        self._api.install()

    def _update(self, command: UpdateCommand) -> None:
        pass
        self._api.update()

    def _check(self, command: CheckCommand) -> None:
        pass
        self._api.validate()

class PoetryPlugin(Plugin):
    def valid(self, data: dict) -> bool:
        return data["build-system"]["build-backend"] == "poetry.core.masonry.api"

    def gather_pep_612(self, data: dict) -> dict:
        return PEP621(
            data["tool"]["poetry"]["name"], 
            data["tool"]["poetry"]["version"],
            data["tool"]["poetry"]["description"],
            data["tool"]["poetry"]["readme"],
            data["tool"]["poetry"]["dependencies"]['python'],
            data["tool"]["poetry"]["license"],
            data["tool"]["poetry"]["authors"],
            data["tool"]["poetry"]["maintainers"],
            data["tool"]["poetry"]["keywords"],
            data["tool"]["poetry"]["classifiers"],
            data["tool"]["poetry"]["urls"]
        )
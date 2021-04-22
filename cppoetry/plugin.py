from tomlkit import parse

from cleo.events.console_events import COMMAND
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.poetry import Poetry

from pathlib import Path


class SynodicPlugin(ApplicationPlugin):

    data = None
    generators = ["cmake_find_package", "cmake_paths"]

    def __init__(self):
        """
        TODO: Remove hardcoded extraction once poetry has plugin support
        """

        if not SynodicPlugin.data:
            with open("pyproject.toml", "r") as file:
                SynodicPlugin.data = parse(file.read())

            # Generate the conanfile.py
            self.__write_conanfile(Path(SynodicPlugin.data["tool"]["conan"]["install-path"]))

    def __write_conanfile(self, path: Path):
        """
        Generate a conanfile.py with the given path.
        The resulting recipe is TODO
        """
        path = path.absolute()
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "conanfile.py", "w+") as file:

            # Process the Conan data into a Conan format
            name = SynodicPlugin.data["tool"]["poetry"]["name"]
            name = name.replace("-", "")

            dependencies = ["/".join(tup) for tup in SynodicPlugin.data["tool"]["conan"]["dependencies"].items()]
            dependencies = ",".join('"{0}"'.format(w) for w in dependencies)

            generators = ",".join('"{0}"'.format(g) for g in SynodicPlugin.generators)

            # Write the Conan data to file
            contents = (
                f"from conans import ConanFile, CMake\n"
                f"\n"
                f"class {name}Conan(ConanFile):\n"
                f'    settings = "os", "compiler", "build_type", "arch"\n'
                f"    requires = {dependencies}\n"
                f"    generators = {generators}\n"
            )

            print(contents, file=file)

    def activate(self, application: Application):
        """
        The entry function for the Poetry plugin
        """

        application.event_dispatcher.add_listener(COMMAND, self.new)

    def new(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def init(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def install(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def update(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def add(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def remove(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def show(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def build(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def publish(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def config(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def run(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def shell(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def check(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def search(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def lock(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def version(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def export(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def env(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

    def cache(self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher) -> None:

        pass

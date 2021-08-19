from cppython.project import Project
from cppython.schema import Interface, PEP621
from pathlib import Path

import click


class Config(object):
    def __init__(self):
        self.project = Project(Path.cwd())


@click.group()
@click.pass_context
def cli(context):
    context.obj = Config()


@cli.command()
@click.pass_obj
def install(obj):
    obj.project.generator.install()


@cli.command()
@click.pass_obj
def update(obj):
    obj.project.generator.update()


@cli.result_callback()
@click.pass_obj
def cleanup(obj, result):
    if obj.project.dirty:
        obj.projectFile.write(obj.document)


class ConsoleInterface(Interface):
    """
    TODO: Description
    """

    def __init__(self) -> None:
        pass

    """
    Plugin Contract
    """

    @staticmethod
    def name() -> str:
        """
        The name of the generator
        """
        return "console"

    """
    Interface Contract
    """

    @staticmethod
    def external_config() -> bool:
        """
        True if the plugin can read its own configuration.
        False otherwise
        """

        return False

    @staticmethod
    def parse_pep_612(self, data: dict) -> PEP621:
        """
        Requests the plugin to read the available PEP 612 information. Only requested if the plugin is not the entrypoint
        """
        raise NotImplementedError()

    def pep_612_data(self) -> PEP621:
        """
        Requests PEP 612 information from the pyproject
        """
        raise NotImplementedError()

    def write_pyproject(self) -> None:
        raise NotImplementedError()

    def read_pyproject(self, path: Path) -> dict:
        if path.is_file():
            path = path.parent

        while not path.glob("pyproject.toml"):
            if path.is_absolute():
                assert "This is not a valid project. No pyproject.toml found in the current directory or any of its parents."

        import tomlkit

        return tomlkit.loads(Path(path / "pyproject.toml").read_text(encoding="utf-8"))

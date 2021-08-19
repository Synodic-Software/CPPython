from cppython.project import Project
from cppython.schema import Interface, PEP621
from pathlib import Path

import click


class Config(object):
    """
    The data object that will be expanded alongside 'pass_obj'
    """

    def __init__(self):
        self.project = Project(ConsoleInterface)


pass_config = click.make_pass_decorator(Config)

@click.group()
@click.pass_context
def cli(context):
    context.obj = Config()


@cli.command()
@pass_config
def install(config):
    config.project.install()


@cli.command()
@pass_config
def update(config):
    config.project.update()


@cli.result_callback()
@pass_config
def cleanup(config, result):
    pass


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

    def read_pyproject(self) -> dict:
        path = Path.cwd()

        while not path.glob("pyproject.toml"):
            if path.is_absolute():
                assert "This is not a valid project. No pyproject.toml found in the current directory or any of its parents."

        import tomlkit

        return tomlkit.loads(Path(path / "pyproject.toml").read_text(encoding="utf-8"))

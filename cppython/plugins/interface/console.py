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


@cli.resultcallback()
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

    def gather_pep_612(self, data: dict) -> PEP621:
        raise NotImplementedError()

    def write_pyproject(self, data: dict) -> None:
        raise NotImplementedError()

    def read_pyproject(self, path: Path) -> dict:
        if path.is_file():
            path = path.parent

        while not path.glob("pyproject.toml"):
            if path.is_absolute():
                assert "This is not a valid project. No pyproject.toml found in the current directory or any of its parents."

        import tomlkit

        return tomlkit.loads(Path(path / "pyproject.toml").read_text(encoding="utf-8"))

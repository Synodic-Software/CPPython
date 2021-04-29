import click

from cppoetry.core import CPPoetryAPI
from cppoetry.utility import Metadata

from tomlkit.toml_file import TOMLFile

# TODO: Project location management
_projectFile = TOMLFile("pyproject.toml")
_document = _projectFile.read()
_metadata = Metadata(_document)

@click.group()
def cli():
    pass

@cli.command()
def validate():
    CPPoetryAPI(_metadata).validate()

@cli.command()
def install():
    CPPoetryAPI(_metadata).install()

@cli.command()
def update():
    CPPoetryAPI(_metadata).update()

@cli.resultcallback()
def cleanup(result):
    if _metadata.dirty:
        _projectFile.write(_document)
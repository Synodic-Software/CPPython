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
    CPPoetryAPI(_document).validate()

@cli.command()
def install():
    CPPoetryAPI(_document).install()

@cli.command()
def update():
    CPPoetryAPI(_document).update()

@cli.resultcallback()
def cleanup(result):
    if _metadata.dirty:
        _projectFile.write(_document)
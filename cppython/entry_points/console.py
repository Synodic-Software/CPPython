import click

from cppython.core import CPPythonAPI
from cppython.data import Metadata

from tomlkit.toml_file import TOMLFile
from tomlkit.exceptions import NonExistentKey
from pathlib import Path

class Config(object):

    def __init__(self):
        self.cwd = Path.cwd()
        self.projectFile = TOMLFile("pyproject.toml")
        self.document = self.projectFile.read()

        data = {}
        
        try:
            # Strip the the TOMLDocument metadata
            data |= {}
        except NonExistentKey:
            pass

        self.metadata = Metadata(data)

@click.group()
@click.pass_context
def cli(context):
    context.obj = Config()

@cli.command()
@click.pass_obj
def validate(obj):
    CPPythonAPI(obj.cwd, obj.metadata).validate()

@cli.command()
@click.pass_obj
def install(obj):
    CPPythonAPI(obj.cwd, obj.metadata).install()

@cli.command()
@click.pass_obj
def update(obj):
    CPPythonAPI(obj.cwd, obj.metadata).update()

@cli.resultcallback()
@click.pass_obj
def cleanup(obj, result):
    if obj.metadata.dirty:
        obj.projectFile.write(obj.document)
import click
import toml

from cppython.core import CPPythonAPI
from cppython.data import Metadata

from pathlib import Path

class Config(object):

    def __init__(self):
        self.cwd = Path.cwd()        
        data = toml.load(self.cwd / "pyproject.toml")
        self.metadata = Metadata(data['tool']['conan'])

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
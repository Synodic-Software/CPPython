import click

from cppoetry.core import CPPoetryAPI
from cppoetry.utility import Metadata

from tomlkit.toml_file import TOMLFile

class Config(object):

    def __init__(self):
        self.projectFile = TOMLFile("pyproject.toml")
        self.document = self.projectFile.read()
        self.metadata = Metadata(self.document)

@click.group()
@click.pass_context
def cli(context):
    context.obj = Config()

@cli.command()
@click.pass_obj
def validate(obj):
    CPPoetryAPI(obj.metadata).validate()

@cli.command()
@click.pass_obj
def install(obj):
    CPPoetryAPI(obj.metadata).install()

@cli.command()
@click.pass_obj
def update(obj):
    CPPoetryAPI(obj.metadata).update()

@cli.resultcallback()
@click.pass_obj
def cleanup(obj, result):
    if obj.metadata.dirty:
        obj.projectFile.write(obj.document)
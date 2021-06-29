import click

from cppython.project import Project

from pathlib import Path

class Config(object):

    def __init__(self):
        self.cwd = Path.cwd()        
        self.project = Project(self.cwd / "pyproject.toml")

@click.group()
@click.pass_context
def cli(context):
    context.obj = Config()

@cli.command()
@click.pass_obj
def install(obj):
    obj.project.install()

@cli.command()
@click.pass_obj
def update(obj):
    obj.project.update()

@cli.resultcallback()
@click.pass_obj
def cleanup(obj, result):
    if obj.project.dirty:
        obj.projectFile.write(obj.document)
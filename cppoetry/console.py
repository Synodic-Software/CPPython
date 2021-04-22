import click

from cppoetry.core import api

@click.group()
def cli():
    api.check()

@cli.command()
def new():
    click.echo('new is not yet a supported command')

@cli.command()
def init():
    click.echo('init is not yet a supported command')

@cli.command()
def install():
    click.echo('install is not yet a supported command')

@cli.command()
def update():
    click.echo('update is not yet a supported command')

@cli.command()
def add():
    click.echo('add is not yet a supported command')

@cli.command()
def remove():
    click.echo('remove is not yet a supported command')

@cli.command()
def show():
    click.echo('show is not yet a supported command')

@cli.command()
def build():
    click.echo('build is not yet a supported command')

@cli.command()
def publish():
    click.echo('publish is not yet a supported command')

@cli.command()
def config():
    click.echo('config is not yet a supported command')

@cli.command()
def run():
    click.echo('run is not yet a supported command')

@cli.command()
def shell():
    click.echo('shell is not yet a supported command')

@cli.command()
def check():
    click.echo('check is not yet a supported command')

@cli.command()
def search():
    click.echo('search is not yet a supported command')

@cli.command()
def lock():
    click.echo('lock is not yet a supported command')

@cli.command()
def version():
    click.echo('version is not yet a supported command')

@cli.command()
def export():
    click.echo('export is not yet a supported command')

@cli.command()
def env():
    click.echo('env is not yet a supported command')

@cli.command()
def cache():
    click.echo('cache is not yet a supported command')
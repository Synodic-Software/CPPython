import click

from cppoetry.core import api

@click.group()
def cli():
    api.check()

@cli.command()
def check():
    click.echo('Check')

@cli.command()
def install():
    click.echo('Install')
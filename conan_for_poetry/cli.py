# TODO: Remove CLI interface once poetry has plugin support

import click
import sys
import subprocess

from conan_for_poetry.plugin import ConanPlugin


@click.group()
def entrypoint():
    command = ['poetry']
    command.extend(sys.argv[1:])
    subprocess.run(command)


@entrypoint.command()
def new():
    ConanPlugin().poetry_new()


@entrypoint.command()
def init():
    ConanPlugin().poetry_init()


@entrypoint.command()
def install():
    ConanPlugin().poetry_install()


@entrypoint.command()
def update():
    ConanPlugin().poetry_update()


@entrypoint.command()
def add():
    ConanPlugin().poetry_add()


@entrypoint.command()
def remove():
    ConanPlugin().poetry_remove()


@entrypoint.command()
def show():
    ConanPlugin().poetry_show()


@entrypoint.command()
def build():
    ConanPlugin().poetry_build()


@entrypoint.command()
def publish():
    ConanPlugin().poetry_publish()


@entrypoint.command()
def config():
    ConanPlugin().poetry_config()


@entrypoint.command()
def check():
    ConanPlugin().poetry_check()


@entrypoint.command()
def search():
    ConanPlugin().poetry_search()


@entrypoint.command()
def lock():
    ConanPlugin().poetry_lock()


@entrypoint.command()
def version():
    ConanPlugin().poetry_version()


@entrypoint.command()
def export():
    ConanPlugin().poetry_export()


@entrypoint.command()
def env():
    ConanPlugin().poetry_env()

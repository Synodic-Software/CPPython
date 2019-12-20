#TODO: Remove CLI interface once poetry has plugin support

import click

from conan_for_poetry.plugin import ConanPlugin


@click.group()
def entrypoint():
    pass


@entrypoint.command()
def poetry_new(self):
    ConanPlugin().poetry_new()


@entrypoint.command()
def Init(self):
    ConanPlugin.poetry_init()


@entrypoint.command()
def Install():
    ConanPlugin().poetry_install()


@entrypoint.command()
def Update():
    ConanPlugin().poetry_update()


@entrypoint.command()
def poetry_add(self):
    ConanPlugin().poetry_add()


@entrypoint.command()
def poetry_remove(self):
    ConanPlugin().poetry_remove()


@entrypoint.command()
def poetry_show(self):
    ConanPlugin().poetry_show()


@entrypoint.command()
def poetry_build(self):
    ConanPlugin().poetry_build()


@entrypoint.command()
def poetry_publish(self):
    ConanPlugin().poetry_publish()


@entrypoint.command()
def poetry_config(self):
    ConanPlugin().poetry_config()


@entrypoint.command()
def poetry_check(self):
    ConanPlugin().poetry_check()


@entrypoint.command()
def poetry_search(self):
    ConanPlugin().poetry_search()

    
@entrypoint.command()
def poetry_lock(self):
    ConanPlugin().poetry_lock()


@entrypoint.command()
def poetry_version(self):
    ConanPlugin().poetry_version()


@entrypoint.command()
def poetry_export(self):
    ConanPlugin().poetry_export()


@entrypoint.command()
def poetry_env(self):
    ConanPlugin().poetry_env()

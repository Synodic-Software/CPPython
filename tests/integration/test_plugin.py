import pytest

from conan_for_poetry.plugin import SynodicPlugin
from path import Path
from distutils.dir_util import copy_tree


@pytest.fixture
def test_project(tmp_path):

    template_directory = Path("tests/template/test_project").abspath()
    directory = Path(tmp_path).abspath()
    copy_tree(template_directory, directory)

    with directory:
        yield tmp_path


class TestPlugin():

    def test_poetry_new(self):

        SynodicPlugin().poetry_new()

    def test_poetry_init(self):

        SynodicPlugin().poetry_init()

    def test_poetry_install(self, test_project):

        SynodicPlugin().poetry_install()

    def test_poetry_update(self, test_project):

        SynodicPlugin().poetry_update()

    def test_poetry_add(self):

        SynodicPlugin().poetry_add()

    def test_poetry_remove(self):

        SynodicPlugin().poetry_remove()

    def test_poetry_show(self):

        SynodicPlugin().poetry_show()

    def test_poetry_build(self):

        SynodicPlugin().poetry_build()

    def test_poetry_publish(self):

        SynodicPlugin().poetry_publish()

    def test_poetry_config(self):

        SynodicPlugin().poetry_config()

    def test_poetry_check(self):

        SynodicPlugin().poetry_check()

    def test_poetry_search(self):

        SynodicPlugin().poetry_search()

    def test_poetry_lock(self):

        SynodicPlugin().poetry_lock()

    def test_poetry_version(self):

        SynodicPlugin().poetry_version()

    def test_poetry_export(self):

        SynodicPlugin().poetry_export()

    def test_poetry_env(self):

        SynodicPlugin().poetry_env()

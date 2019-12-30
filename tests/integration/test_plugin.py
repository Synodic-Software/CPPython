import pytest

from conan_for_poetry.plugin import ConanPlugin
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

        ConanPlugin().poetry_new()

    def test_poetry_init(self):

        ConanPlugin().poetry_init()

    def test_poetry_install(self, test_project):

        ConanPlugin().poetry_install()

    def test_poetry_update(self, test_project):

        ConanPlugin().poetry_update()

    def test_poetry_add(self):

        ConanPlugin().poetry_add()

    def test_poetry_remove(self):

        ConanPlugin().poetry_remove()

    def test_poetry_show(self):

        ConanPlugin().poetry_show()

    def test_poetry_build(self):

        ConanPlugin().poetry_build()

    def test_poetry_publish(self):

        ConanPlugin().poetry_publish()

    def test_poetry_config(self):

        ConanPlugin().poetry_config()

    def test_poetry_check(self):

        ConanPlugin().poetry_check()

    def test_poetry_search(self):

        ConanPlugin().poetry_search()

    def test_poetry_lock(self):

        ConanPlugin().poetry_lock()

    def test_poetry_version(self):

        ConanPlugin().poetry_version()

    def test_poetry_export(self):

        ConanPlugin().poetry_export()

    def test_poetry_env(self):

        ConanPlugin().poetry_env()

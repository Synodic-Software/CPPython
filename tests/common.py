import pytest

from path import Path
from distutils.dir_util import copy_tree


@pytest.fixture
def test_project(tmp_path):
    '''
    Load the dummy project to its initial state
    '''

    template_directory = Path("tests/data/test_project").abspath()
    directory = Path(tmp_path).abspath()
    copy_tree(template_directory, directory)

    yield directory

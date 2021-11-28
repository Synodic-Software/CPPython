import pytest

from pathlib import Path
from distutils.dir_util import copy_tree


@pytest.fixture
def tmp_workspace(tmp_path):
    '''
    Load the dummy project to its initial state
    '''

    template_directory = Path("tests/data/test_project").absolute()
    directory = Path(tmp_path).absolute()
    copy_tree(str(template_directory), str(directory))

    return directory

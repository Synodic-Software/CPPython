import pytest
from os import scandir

from pathlib import Path
from distutils.dir_util import copy_tree

def _extract_directories(directory):
    directories = [Path(f) for f in scandir(directory) if f.is_dir() ]
    return directories

_directories = _extract_directories(Path("tests/data/project_templates").absolute())

def pytest_generate_tests(metafunc):

    # Provides a directory taken from the 'tests/data' directory
    if "directory" in metafunc.fixturenames:
        metafunc.parametrize("directory", _directories, ids = [id.name for id in _directories])


@pytest.fixture
def tmp_workspace(tmp_path, directory):
    '''
    Load the dummy project to its initial state
    '''
    base_directory = Path(tmp_path).absolute()
    copy_tree(str(directory), str(base_directory))

    return base_directory

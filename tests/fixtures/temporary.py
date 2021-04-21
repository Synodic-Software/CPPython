import pytest
import subprocess
import os
import contextlib

from pathlib import Path
from distutils.dir_util import copy_tree

from typing import Generator


def _extract_directories(directory):
    directories = [Path(f) for f in os.scandir(directory) if f.is_dir()]
    return directories


@contextlib.contextmanager
def _working_directory(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


_directories = _extract_directories(Path("tests/data/project_templates").absolute())


def pytest_generate_tests(metafunc):

    if "directory" in metafunc.fixturenames:
        metafunc.parametrize("directory", _directories, ids=[id.name for id in _directories])


@pytest.fixture
def tmp_library(tmp_path: Path, directory: Path) -> Path:
    """
    @returns - A path to the temporary directory populated with a test library
    """
    target_directory = Path(tmp_path).absolute()
    copy_tree(str(directory), str(target_directory))

    return target_directory

@pytest.fixture
def tmp_workspace(tmp_library: Path) -> Generator[Path, None, None]:
    """
    While the fixture is used, the current directory exists as a temporary workspace populated with a library and a virtual environment

    @returns - The name of the library
    """
    with _working_directory(tmp_library):
        yield tmp_library
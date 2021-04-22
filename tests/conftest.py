import pytest

import subprocess
import os
import contextlib

from pathlib import Path
from distutils.dir_util import copy_tree
from typing import Generator


def _extract_directories(directory: Path):
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

    if "test_workspace" in metafunc.fixturenames:
        metafunc.parametrize("test_workspace", _directories, ids=[id.name for id in _directories])


@pytest.fixture
def tmp_workspace(tmp_path: Path, test_workspace: Path) -> Path:
    """
    @returns - A path to the temporary directory populated with a test workspace
    """
    target_directory = Path(tmp_path).absolute()
    copy_tree(str(test_workspace), str(target_directory))

    with _working_directory(test_workspace):
        yield target_directory

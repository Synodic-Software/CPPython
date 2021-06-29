import pytest
import contextlib
import os

from cppython.project import Project

from pathlib import Path
from distutils.dir_util import copy_tree

# Fixtures
class WorkspaceData:
    def __init__(self, path: Path, project: Project):
        self.path = path
        self.project = project


@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


# Tests
@pytest.fixture
def tmp_workspace(tmp_path: Path, test_workspace: Path):
    """
    @returns - A path to the temporary directory populated with a test workspace
    """
    target_directory = Path(tmp_path).absolute()
    copy_tree(str(test_workspace), str(target_directory))

    with working_directory(target_directory):
        project = Project(Path.cwd())

        yield WorkspaceData(target_directory, project)


class TestWorkflow:

    pass
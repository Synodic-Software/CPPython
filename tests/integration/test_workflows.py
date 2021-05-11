import pytest
import contextlib
import os

from cppython.core import CPPythonAPI
from cppython.data import Metadata
from tomlkit.toml_file import TOMLFile
from tomlkit.exceptions import NonExistentKey
from pathlib import Path
from distutils.dir_util import copy_tree

# Fixtures
class WorkspaceData:
    def __init__(self, path: Path, metadata: Metadata):
        self.path = path
        self.metadata = metadata


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
        projectFile = TOMLFile("pyproject.toml")
        document = projectFile.read()

        data = {}
        
        try:
            # Strip the the TOMLDocument metadata
            data |= {}
        except NonExistentKey:
            pass

        metadata = Metadata(data)

        yield WorkspaceData(target_directory, metadata)


class TestWorkflow:
    def test_validation_workflow(self, tmp_workspace):
        CPPythonAPI(tmp_workspace.path, tmp_workspace.metadata).validate()

    def test_development_workflow(self, tmp_workspace):

        api = CPPythonAPI(tmp_workspace.path, tmp_workspace.metadata)

        api.install()
        api.update()

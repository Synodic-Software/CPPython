import pytest
from os import scandir

from pathlib import Path
from distutils.dir_util import copy_tree

from typing import Generator

from poetry.poetry import Poetry
from poetry.packages.locker import Locker
from poetry.packages.project_package import ProjectPackage
from poetry.config.config import Config

def _extract_directories(directory):
    directories = [Path(f) for f in scandir(directory) if f.is_dir()]
    return directories


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


class workspaceInfo:
    def __init__(self, name, poetry):
        self.name = name
        self.poetry = poetry

@pytest.fixture
def tmp_workspace(tmp_library: Path) -> Generator[workspaceInfo, None, None]:
    """
    While the fixture is used, the current directory exists as a temporary workspace populated with a library and a virtual environment

    @returns - The name of the library
    """
    with tmp_library:
        poetry = Poetry(
                "pyproject.toml",
                {},
                ProjectPackage(tmp_library.name, "0.1.0"),
                Locker("poetry.lock", {}),
                Config(False, Path().absolute())
        )


        yield workspaceInfo(tmp_library.name, poetry)
import pytest
import os

from pathlib import Path

def _extract_directories(directory: Path):
    directories = [Path(f) for f in os.scandir(directory) if f.is_dir()]
    return directories

_directories = _extract_directories(Path("tests/data/project_templates").absolute())

def pytest_generate_tests(metafunc):

    if "test_workspace" in metafunc.fixturenames:
        metafunc.parametrize("test_workspace", _directories, ids=[id.name for id in _directories])
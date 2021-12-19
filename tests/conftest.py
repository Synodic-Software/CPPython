"""
TODO: 
"""

from pathlib import Path
from shutil import copytree

import pytest


@pytest.fixture
def tmp_workspace(tmp_path):
    """
    Load the dummy project to its initial state
    """

    template_directory = Path("tests/data/test_project").absolute()
    directory = Path(tmp_path).absolute()
    copytree(str(directory), str(template_directory), dirs_exist_ok=True)

    return directory

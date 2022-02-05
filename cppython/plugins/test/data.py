"""
TODO
"""

from pathlib import Path

from cppython.schema import PEP621, Metadata, PyProject, TargetEnum

default_pyproject = PyProject(data={})

default_pep621 = PEP621(name="Ya", version="1.0")

default_metadata = Metadata(target=TargetEnum.EXE, install_path=Path())

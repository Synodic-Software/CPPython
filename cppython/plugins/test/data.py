"""
TODO
"""

from pathlib import Path

from cppython.schema import PEP621, CPPythonData, TargetEnum

default_pep621 = PEP621(name="Ya", version="1.0")

default_cppython_data = CPPythonData(generator="cmake", target=TargetEnum.EXE, install_path=Path())

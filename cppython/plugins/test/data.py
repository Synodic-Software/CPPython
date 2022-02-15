"""
Defaulted data to help testing
"""

from pathlib import Path

from cppython.schema import PEP621, CPPythonData, PyProject, TargetEnum

default_pep621 = PEP621(name="test_name", version="1.0")

# CMake is a default plugin
# TODO: Provide dynamic default
default_cppython_data = CPPythonData(generator="cmake", target=TargetEnum.EXE, install_path=Path())

default_pyproject = PyProject(pep_621=default_pep621, cppython_data=default_cppython_data)

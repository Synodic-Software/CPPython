"""
Defaulted data to help testing
"""

from pathlib import Path

from cppython_core.schema import PEP621, CPPythonData, PyProject, TargetEnum, ToolData

default_pep621 = PEP621(name="test_name", version="1.0")

# CMake is a default plugin
default_cppython_data = CPPythonData(**{"generator": "cmake", "target": TargetEnum.EXE, "install-path": Path()})
default_tool_data = ToolData(**{"cppython": default_cppython_data})
default_pyproject = PyProject(**{"project": default_pep621, "tool": default_tool_data})

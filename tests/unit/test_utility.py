"""TODO
"""
from pathlib import Path

from cppython_core.schema import CPPythonModel

from cppython.utility import read_model_json, write_model_json


class TestBuilder:
    """_summary_"""

    class ModelTest(CPPythonModel):
        """_summary_

        Args:
            CPPythonModel: _description_
        """

        test_path: Path
        test_int: int

    def test_model_read_write(self, tmp_path: Path) -> None:
        """_summary_

        Args:
            tmp_path: _description_
        """

        test_model = TestBuilder.ModelTest(test_path=Path(), test_int=3)

        json_path = tmp_path / "test.json"

        write_model_json(json_path, test_model)
        output = read_model_json(json_path, TestBuilder.ModelTest)

        assert test_model == output

    def test_something(self) -> None:
        """_summary_"""

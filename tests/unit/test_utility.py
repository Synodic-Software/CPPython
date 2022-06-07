"""
TODO
"""
from pathlib import Path

from cppython_core.schema import CPPythonModel

from cppython.utility import read_model_json, write_model_json


class TestBuilder:
    """
    TODO
    """

    class TestModel(CPPythonModel):
        """
        TODO
        """

        test_path: Path
        test_int: int

    def test_model_read_write(self, tmpdir):
        """
        TODO
        """

        test_model = TestBuilder.TestModel(test_path=Path(), test_int=3)

        temporary_directory = Path(tmpdir)

        json_path = temporary_directory / "test.json"

        write_model_json(json_path, test_model)
        output = read_model_json(json_path, TestBuilder.TestModel)

        assert test_model == output

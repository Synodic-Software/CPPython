"""
TODO
"""
from pathlib import Path

from pydantic.main import BaseModel

from cppython.utility import read_model_json, write_model_json


class TestBuilder:
    """
    TODO
    """

    def test_model_read_write(self, tmpdir):
        """
        TODO
        """

        class TestModel(BaseModel):
            """
            TODO
            """

            test_path: Path
            test_int: int

        test_model = TestModel(test_path=Path(), test_int=3)

        temporary_directory = Path(tmpdir)

        json_path = temporary_directory / "test.json"

        write_model_json(json_path, test_model)
        output = read_model_json(json_path, TestModel)

        assert test_model == output

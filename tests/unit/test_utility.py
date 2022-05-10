"""
TODO
"""
from pathlib import Path

from cppython.schema import CMakePresets
from cppython.utility import read_preset, write_preset, write_presets


class TestBuilder:
    """
    TODO
    """

    def test_preset_read_write(self, tmpdir):
        """
        TODO
        """

        temporary_directory = Path(tmpdir)

        presets = CMakePresets()
        write_preset("test", temporary_directory, presets)
        output = read_preset("test", temporary_directory)

        assert presets == output

    def test_presets(self, tmpdir):
        """
        TODO
        """

        temporary_directory = Path(tmpdir)

        input_toolchain = temporary_directory / "input.cmake"

        with open(input_toolchain, "w", encoding="utf8") as file:
            file.write("")

        generator_output = [("test", input_toolchain)]
        write_presets(temporary_directory, generator_output)

        cppython_tool = temporary_directory / "cppython"
        assert cppython_tool.exists()

        cppython_file = cppython_tool / "cppython.json"
        assert cppython_file.exists()

        test_tool = cppython_tool / "test"
        assert test_tool.exists()

        test_file = test_tool / "test.json"
        assert test_file.exists()

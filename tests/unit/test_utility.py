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

    def test_preset_read_write(self, tmpdir: Path):
        """
        TODO
        """

        presets = CMakePresets()
        write_preset("test", tmpdir, presets)
        output = read_preset("test", tmpdir)

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

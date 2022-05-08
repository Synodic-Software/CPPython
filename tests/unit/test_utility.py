"""
TODO
"""
from pathlib import Path

from cppython.schema import CMakePresets
from cppython.utility import read_preset, write_preset


class TestBuilder:
    """
    TODO
    """

    def test_preset_read_write(self, tmpdir: Path):
        """
        TODO
        """

        presets = CMakePresets()
        write_preset(tmpdir, presets)
        output = read_preset(tmpdir)

        assert presets == output

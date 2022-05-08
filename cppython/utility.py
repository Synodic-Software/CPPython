"""
TODO
"""

import json
from pathlib import Path

from cppython.schema import CMakePresets


def read_preset(path: Path) -> CMakePresets:
    """
    Reading routing
    """

    preset_path = path / "CMakePresets.json"
    return CMakePresets.parse_file(path=preset_path)


def write_preset(path: Path, presets: CMakePresets) -> None:
    """
    Writing routine
    """
    with open(path / "CMakePresets.json", "w", encoding="utf8") as json_file:
        json.dump(presets.dict(), json_file, ensure_ascii=False, indent=2)

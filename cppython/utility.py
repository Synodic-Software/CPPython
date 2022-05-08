"""
TODO
"""

import json
from pathlib import Path

from cppython.schema import CMakePresets


def read_preset(name: str, path: Path) -> CMakePresets:
    """
    Reading routing
    """

    preset_path = path / f"{name}.json"
    return CMakePresets.parse_file(path=preset_path)


def write_preset(name: str, path: Path, presets: CMakePresets) -> Path:
    """
    Writing routine
    """
    file = path / f"{name}.json"

    with open(file, "w", encoding="utf8") as json_file:
        json.dump(presets.dict(), json_file, ensure_ascii=False, indent=2)

    return file

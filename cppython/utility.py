"""
TODO
"""

import json
from pathlib import Path

from cppython.schema import CMakePresets, ConfigurePreset


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

    serialized = json.loads(presets.json(exclude_none=True))
    with open(file, "w", encoding="utf8") as json_file:
        json.dump(serialized, json_file, ensure_ascii=False, indent=2)

    return file


def write_presets(tool_path: Path, generator_output: list[tuple[str, Path]]) -> None:
    """
    Write the cppython presets
    """

    def write_generator_presets(tool_path: Path, generator_name: str, toolchain_path: Path) -> Path:
        """
        Write a generator preset.
        @returns - The written json file
        """
        generator_tool_path = tool_path / generator_name
        generator_tool_path.mkdir(parents=True, exist_ok=True)

        configure_preset = ConfigurePreset(name=generator_name, hidden=True, toolchainFile=str(toolchain_path))
        presets = CMakePresets(configurePresets=[configure_preset])

        return write_preset(generator_name, generator_tool_path, presets)

    names = []
    includes = []

    tool_path = tool_path / "cppython"

    for generator_name, toolchain in generator_output:

        preset_file = write_generator_presets(tool_path, generator_name, toolchain)

        relative_file = preset_file.relative_to(tool_path)

        names.append(generator_name)
        includes.append(str(relative_file))

    configure_preset = ConfigurePreset(name="cppython", hidden=True, inherits=names)
    presets = CMakePresets(configurePresets=[configure_preset], include=includes)

    write_preset("cppython", tool_path, presets)

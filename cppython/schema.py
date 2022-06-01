"""
TODO
"""

from __future__ import annotations  # Required for self-referenced pydantic types

from abc import abstractmethod
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Extra, Field, validator


class Preset(BaseModel):
    """
    Partial Preset specification
    """

    name: str
    hidden: Optional[bool]
    inherits: Optional[list[str] | str]
    displayName: Optional[str]
    description: Optional[str]

    @validator("inherits")
    def validate_str(cls, values):  # pylint: disable=E0213
        """
        Conform to list
        """
        if isinstance(values, str):
            return [values]

        return values


class ConfigurePreset(Preset):
    """
    Partial Configure Preset specification
    """

    toolchainFile: Optional[str]

    @validator("toolchainFile")
    def validate_path(cls, value):  # pylint: disable=E0213
        """
        TODO
        """
        if value is not None:
            return Path(value).as_posix()

        return None


class BuildPreset(Preset):
    """
    Partial Build Preset specification
    """

    configurePreset: Optional[str]
    inheritConfigureEnvironment: Optional[bool]


class TestPreset(Preset):
    """
    Partial Test Preset specification
    """

    configurePreset: Optional[str]
    inheritConfigureEnvironment: Optional[bool]


class CMakeVersion(BaseModel, extra=Extra.forbid):
    """
    The version specification for CMake
    """

    major: int = 3
    minor: int = 23
    patch: int = 1


class CMakePresets(BaseModel, extra=Extra.forbid):
    """
    The schema for the CMakePresets and CMakeUserPresets files
    """

    version: int = Field(default=4, const=True)
    cmakeMinimumRequired: CMakeVersion = CMakeVersion()  # TODO: 'version' compatibility validation
    include: Optional[list[str]]
    vendor: Optional[Any]
    configurePresets: Optional[list[ConfigurePreset]]
    buildPresets: Optional[list[BuildPreset]]
    testPresets: Optional[list[TestPreset]]

    @validator("include")
    def validate_path(cls, values):  # pylint: disable=E0213
        """
        TODO
        """
        if values is not None:
            output = []
            for value in values:
                output.append(Path(value).as_posix())
            return output

        return None


class ProjectConfiguration(BaseModel):
    """
    TODO
    """

    root_path: Path  # The path where the pyproject.toml lives
    version: str  # The version number a 'dynamic' project version will resolve to
    verbosity: int = 0

    @validator("verbosity")
    def min_max(cls, value):  # pylint: disable=E0213
        """
        TODO
        """
        return min(max(value, 0), 2)


class API:
    """
    Project API
    """

    @abstractmethod
    def install(self) -> None:
        """
        TODO
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self) -> None:
        """
        TODO
        """

        raise NotImplementedError()

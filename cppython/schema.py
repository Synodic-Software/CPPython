"""
TODO
"""

from __future__ import annotations  # Required for self-referenced pydantic types

from abc import abstractmethod
from pathlib import Path
from typing import Any, Optional

from cppython_core.schema import ConfigurePreset, CPPythonModel, Preset
from pydantic import Extra, Field, validator


class BuildPreset(Preset):
    """
    Partial Build Preset specification
    """

    configurePreset: Optional[str] = Field(default=None)
    inheritConfigureEnvironment: Optional[bool] = Field(default=None)


class TestPreset(Preset):
    """
    Partial Test Preset specification
    """

    configurePreset: Optional[str] = Field(default=None)
    inheritConfigureEnvironment: Optional[bool] = Field(default=None)


class CMakeVersion(CPPythonModel, extra=Extra.forbid):
    """
    The version specification for CMake
    """

    major: int = Field(default=3)
    minor: int = Field(default=23)
    patch: int = Field(default=1)


class CMakePresets(CPPythonModel, extra=Extra.forbid):
    """
    The schema for the CMakePresets and CMakeUserPresets files
    """

    version: int = Field(default=4, const=True)
    cmakeMinimumRequired: CMakeVersion = Field(default=CMakeVersion())  # TODO: 'version' compatibility validation
    include: Optional[list[str]] = Field(default=None)
    vendor: Optional[Any] = Field(default=None)
    configurePresets: Optional[list[ConfigurePreset]] = Field(default=None)
    buildPresets: Optional[list[BuildPreset]] = Field(default=None)
    testPresets: Optional[list[TestPreset]] = Field(default=None)

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


class ProjectConfiguration(CPPythonModel):
    """
    TODO
    """

    root_path: Path  # The path where the pyproject.toml lives
    version: str  # The version number a 'dynamic' project version will resolve to
    verbosity: int = Field(default=0)

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

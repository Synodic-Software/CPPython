"""Project schema specifications
"""

from __future__ import annotations  # Required for self-referenced pydantic types

from abc import abstractmethod
from pathlib import Path
from typing import Any

from cppython_core.schema import ConfigurePreset, CPPythonModel, Preset
from pydantic import Extra, Field, validator


class BuildPreset(Preset):
    """Partial Build Preset specification

    Args:
        Preset: _description_
    """

    configurePreset: str | None = Field(default=None)
    inheritConfigureEnvironment: bool | None = Field(default=None)


class TestPreset(Preset):
    """Partial Test Preset specification

    Args:
        Preset: _description_
    """

    configurePreset: str | None = Field(default=None)
    inheritConfigureEnvironment: bool | None = Field(default=None)


class CMakeVersion(CPPythonModel, extra=Extra.forbid):
    """The version specification for CMake

    Args:
        CPPythonModel: _description_
        extra: _description_. Defaults to Extra.forbid.
    """

    major: int = Field(default=3)
    minor: int = Field(default=23)
    patch: int = Field(default=1)


class CMakePresets(CPPythonModel, extra=Extra.forbid):
    """The schema for the CMakePresets and CMakeUserPresets files

    Args:
        CPPythonModel: _description_
        extra: _description_. Defaults to Extra.forbid.

    Returns:
        _description_
    """

    version: int = Field(default=4, const=True)
    cmakeMinimumRequired: CMakeVersion = Field(default=CMakeVersion())
    include: list[str] | None = Field(default=None)
    vendor: Any | None = Field(default=None)
    configurePresets: list[ConfigurePreset] | None = Field(default=None)
    buildPresets: list[BuildPreset] | None = Field(default=None)
    testPresets: list[TestPreset] | None = Field(default=None)

    @validator("include")
    @classmethod
    def validate_path(cls, values: list[str] | None) -> list[str] | None:
        """Validates that the path is in posix form

        Args:
            values: _description_

        Returns:
            _description_
        """
        if values is not None:
            output = []
            for value in values:
                output.append(Path(value).as_posix())
            return output

        return None


class API:
    """Project API specification"""

    @abstractmethod
    def install(self) -> None:
        """_summary_

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self) -> None:
        """_summary_

        Raises:
            NotImplementedError: _description_
        """

        raise NotImplementedError()

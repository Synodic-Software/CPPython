"""
Data types for CPPython that encapsulate the requirements between the plugins and the core library
"""

from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Type, TypeVar

from pydantic import BaseModel


class TargetEnum(Enum):
    """
    The C++ build target type
    """

    EXE = "executable"
    STATIC = "static"
    SHARED = "shared"


class PEP621(BaseModel):
    """
    PEP 621 conforming data
        The entirety of PEP 621 is not relevant for interface plugins
        Schema: https://www.python.org/dev/peps/pep-0621/
    """

    name: str
    version: str
    description: str = ""


class CPPythonData(BaseModel):
    """
    Data required by the tool
    """

    generator: str
    target: TargetEnum
    dependencies: dict[str, str] = {}
    install_path: Path


class PyProject(BaseModel):
    """
    pyproject.toml schema
    """

    pep_621: PEP621
    cppython_data: CPPythonData


class API(ABC):
    """
    API
    """

    @abstractmethod
    def install(self) -> None:
        """
        Called when dependencies need to be installed from a lock file.

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self) -> None:
        """
        Called when dependencies need to be updated and written to the lock file.

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError()

    @abstractmethod
    def build(self) -> None:
        """
        Called when the C++ target needs to be produced.

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError()


class Plugin(ABC):
    """
    Abstract plugin type
    """

    @abstractmethod
    def __init__(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def plugin_group() -> str:
        """
        The plugin group name as used by 'setuptools'
        """
        raise NotImplementedError()


class GeneratorData(BaseModel):
    """
    Base class for the configuration data that will be read by the interface and given to the generator
    """


GeneratorDataType = TypeVar("GeneratorDataType", bound=GeneratorData)


class Interface:
    """
    Abstract type to be inherited by CPPython interfaces
    """

    def __init__(self, pyproject: PyProject) -> None:
        super().__init__()

        self.pyproject = pyproject

    @property
    def pyproject(self) -> PyProject:
        """
        PyProject getter
        """
        return self._pyproject

    @pyproject.setter
    def pyproject(self, value: PyProject):
        """
        PyProject setter
        """

        self._pyproject = value

    @abstractmethod
    def read_generator_data(self, generator_data_type: Type[GeneratorDataType]) -> GeneratorDataType:
        """
        Dynamic pyproject.toml data that is determined by the generator plugin requested by [tool.cppython.generator]
            The Schema defined by 'generator_data_type' must be filled by the [tool.cppython.{generator_value}] slot.
        """
        raise NotImplementedError()

    @abstractmethod
    def write_pyproject(self) -> None:
        """
        Called when CPPython requires the interface to write out pyproject.toml changes
        """
        raise NotImplementedError()


class Generator(Plugin, API):
    """
    Abstract type to be inherited by CPPython Generator plugins
    """

    @abstractmethod
    def __init__(self, pyproject: PyProject, generator_data: GeneratorData) -> None:
        super().__init__()

    @staticmethod
    def plugin_group() -> str:
        """
        The plugin group name as used by 'setuptools'
        """
        return "generator_plugins"

    @staticmethod
    @abstractmethod
    def name() -> str:
        """
        The string that is matched with the [tool.cppython.generator] string
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def data_type() -> Type[GeneratorData]:
        """
        Returns the pydantic type to cast the generator configuration data to
        """
        raise NotImplementedError()

    @abstractmethod
    def install_generator(self) -> bool:
        """
        Installs the external tooling required by the generator if necessary
        Returns whether anything was installed or not
        """

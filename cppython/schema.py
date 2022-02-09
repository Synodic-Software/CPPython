"""
Data types for CPPython that encapsulate the requirements between the plugins and the core library
"""

from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, Type

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
    Subset of PEP 621
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
        TODO
        """
        raise NotImplementedError()


class GeneratorData(BaseModel):
    """
    Base class for the configuration data that will be given to the generator constructor
    """


class Interface:
    """
    Abstract type to be inherited by CPPython interfaces
    """

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def pep_621(self) -> PEP621:
        """
        Requests PEP 621 information
        """
        raise NotImplementedError()

    @abstractmethod
    def cppython_data(self) -> CPPythonData:
        """
        Requests CPPython information
        """
        raise NotImplementedError()

    @abstractmethod
    def generator_data(self, generator_data: Type[GeneratorData]) -> GeneratorData:
        """
        Requests generator information
        """
        raise NotImplementedError()

    @abstractmethod
    def write_pyproject(self) -> None:
        """
        Called when CPPython requires the plugin to write out pyproject.toml changes
        """
        raise NotImplementedError()


class Generator(Plugin, API):
    """
    Abstract type to be inherited by CPPython Generator plugins
    """

    @abstractmethod
    def __init__(self, pep_612: PEP621, cppython_data: CPPythonData, generator_data: GeneratorData) -> None:
        super().__init__()

    @staticmethod
    def plugin_group() -> str:
        """
        TODO
        """
        return "generator_plugins"

    @staticmethod
    @abstractmethod
    def name() -> str:
        """
        TODO
        """
        raise NotImplementedError()

    @abstractmethod
    def install_generator(self) -> bool:
        """
        Installs the external tooling required by the generator if necessary
        Returns whether anything was installed or not
        """

    @staticmethod
    @abstractmethod
    def data_type() -> Type[GeneratorData]:
        """
        Returns the pydantic type to cast the generator configuration data to
        """
        raise NotImplementedError()

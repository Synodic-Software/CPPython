from abc import ABC, abstractmethod
from pathlib import Path
from enum import Enum

from pydantic import BaseModel, Field


class TargetEnum(Enum):
    exe = "executable"
    static = "static"
    shared = "shared"


class PEP621(BaseModel):
    """
    Subset of PEP 621
        The entirety of PEP 621 is not relevant for 'interface' plugins
        Schema: https://www.python.org/dev/peps/pep-0621/
    """

    name: str
    version: str
    description: str = ""


class Metadata(BaseModel):
    """
    Metadata required by a generator plugin
    """

    generator: str
    target: TargetEnum
    dependencies: dict[str, str] = []
    install_path: Path = Field(alias="install-path")


class API(ABC):
    """
    API
    """

    @abstractmethod
    def install(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def build(self) -> None:
        raise NotImplementedError()


class Plugin(ABC):
    """
    Abstract plugin type
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def valid(self) -> bool:
        raise NotImplementedError()


class Interface(Plugin):
    """
    Abstract type to be inherited by CPPython Interface plugins
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def gather_pep_612(self) -> PEP621:
        """
        Requests PEP 612 information from the plugin
        """
        raise NotImplementedError()

    @abstractmethod
    def write_pyproject(self, data: dict) -> None:
        """
        Called when CPPoetry requires the plugin to write out pyproject.toml changes
        """
        raise NotImplementedError()

    @abstractmethod
    def read_pyproject(self) -> dict:
        """
        Called when CPPoetry requires the plugin to supply the pyproject.toml data
        """
        raise NotImplementedError()


class Generator(Plugin, API):
    """
    Abstract type to be inherited by CPPython Generator plugins
    """

    def __init__(self) -> None:
        pass

    @property
    @staticmethod
    @abstractmethod
    def name(self) -> str:
        """
        The name of the generator
        """
        raise NotImplementedError()

    @abstractmethod
    def populate_metadata(self, data: dict):
        """
        data - The CPPoetry data taken from pyproject.toml
        """
        raise NotImplementedError()

    @abstractmethod
    def populate_plugin(self, data: dict):
        """
        data - The data taken from pyproject.toml that belongs to this generator
        """
        raise NotImplementedError()

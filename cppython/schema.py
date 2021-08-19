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
        The entirety of PEP 621 is not relevant for interface plugins
        Schema: https://www.python.org/dev/peps/pep-0621/
    """

    name: str
    version: str
    description: str = ""


class Metadata(BaseModel):
    """
    Data required by the tool
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
    def name(self) -> str:
        """
        The name of the generator
        """
        raise NotImplementedError()


class Interface(Plugin):
    """
    Abstract type to be inherited by CPPython Interface plugins
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def external_config() -> bool:
        """
        True if the plugin can read its own configuration.
        False otherwise
        """

        return True

    @staticmethod
    @abstractmethod
    def parse_pep_621(data: dict) -> PEP621:
        """
        Requests the plugin to read the available PEP 621 information. Only requested if the plugin is not the entrypoint
        """
        raise NotImplementedError()

    @abstractmethod
    def pep_621(self) -> PEP621:
        """
        Requests PEP 621 information from the pyproject
        Probably uses 'parse_pep_621' internally
        """
        raise NotImplementedError()

    @abstractmethod
    def read_pyproject(self) -> dict:
        """
        Called when CPPoetry requires the content of pyproject.toml
        """
        raise NotImplementedError()

    @abstractmethod
    def write_pyproject(self) -> None:
        """
        Called when CPPoetry requires the plugin to write out pyproject.toml changes
        """
        raise NotImplementedError()


class Generator(Plugin, API):
    """
    Abstract type to be inherited by CPPython Generator plugins
    """

    @abstractmethod
    def __init__(self, pep_612: PEP621, cppython_data: Metadata, generator_data: dict) -> None:
        pass

    @staticmethod
    @abstractmethod
    def data_type(self):
        """
        Returns the pydantic type to cast the generator configuration data to
        """
        raise NotImplementedError()
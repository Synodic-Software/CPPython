from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, AnyUrl
from pathlib import Path


class Remote(BaseModel):
    name: str
    url = AnyUrl


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

    remotes: list[Remote] = []
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
    def valid(self, data: dict) -> bool:
        raise NotImplementedError()


class Interface(Plugin):
    """
    Abstract type to be inherited by CPPython Interface plugins
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def gather_pep_612(self, data: dict) -> PEP621:
        raise NotImplementedError()


class Generator(Plugin, API):
    """
    Abstract type to be inherited by CPPython Generator plugins
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def metadata(self, data: dict) -> Metadata:
        raise NotImplementedError()

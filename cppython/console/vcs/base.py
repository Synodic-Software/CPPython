"""
TODO
"""


from abc import ABC, abstractmethod
from pathlib import Path

from packaging.version import Version


class VCS(ABC):
    """
    Base class for version control systems
    """

    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    @abstractmethod
    def is_repository(self, path: Path) -> bool:
        """
        TODO
        """
        raise NotImplementedError()

    @abstractmethod
    def extract_version(self, path: Path) -> Version:
        """
        TODO
        """
        raise NotImplementedError()

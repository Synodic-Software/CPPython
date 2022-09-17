"""
TODO
"""


from abc import ABC, abstractmethod
from pathlib import Path

from packaging.version import Version


class VCS(ABC):
    """Base class for version control systems"""

    subclasses: list[type["VCS"]] = []

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    @abstractmethod
    def is_repository(self, path: Path) -> bool:
        """_summary_

        Args:
            path: _description_

        Raises:
            NotImplementedError: _description_

        Returns:
            _description_
        """
        raise NotImplementedError()

    @abstractmethod
    def extract_version(self, path: Path) -> Version:
        """_summary_

        Args:
            path: _description_

        Raises:
            NotImplementedError: _description_

        Returns:
            _description_
        """
        raise NotImplementedError()

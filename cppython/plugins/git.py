"""TODO
"""

from pathlib import Path

from cppython_core.schema import VersionControl
from dulwich.errors import NotGitRepository
from dulwich.repo import Repo


class Git(VersionControl):
    """Git implementation hooks"""

    def is_repository(self, path: Path) -> bool:
        """_summary_

        Args:
            path: _description_

        Returns:
            _description_
        """

        try:
            Repo(str(path))
            return True

        except NotGitRepository:
            return False

    def extract_version(self, path: Path) -> str:
        """_summary_

        Args:
            path: _description_

        Returns:
            _description_
        """
        return "0.1.0"

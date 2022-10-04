"""Git VCS plugin
"""

from pathlib import Path

from cppython_core.plugin_schema.vcs import VersionControl
from dulwich.errors import NotGitRepository
from dulwich.repo import Repo


class Git(VersionControl):
    """Git implementation hooks"""

    @staticmethod
    def name() -> str:
        """The VCS name

        Returns:
            The name
        """
        return "git"

    def is_repository(self, path: Path) -> bool:
        """Queries repository status of a path

        Args:
            path: The input path to query

        Returns:
            Whether the given path is a repository root
        """

        try:
            Repo(str(path))
            return True

        except NotGitRepository:
            return False

    def extract_version(self, path: Path) -> str:
        """Extracts the system's version metadata

        Args:
            path: The repository path

        Returns:
            A version
        """
        return "0.1.0"

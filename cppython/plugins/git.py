"""Git SCM plugin"""

from pathlib import Path

from cppython_core.plugin_schema.scm import SCM
from cppython_core.schema import Information
from dulwich.errors import NotGitRepository
from dulwich.repo import Repo


class GitSCM(SCM):
    """Git implementation hooks"""

    @staticmethod
    def supported(directory: Path) -> bool:
        """Queries repository status of a path

        Args:
            directory: The input path to query

        Returns:
            Whether the given path is a repository root
        """

        try:
            Repo(str(directory))
            return True

        except NotGitRepository:
            return False

    @staticmethod
    def information() -> Information:
        """Extracts the system's version metadata

        Returns:
            A version
        """
        return Information()

    def version(self, path: Path) -> str:
        """Extracts the system's version metadata

        Args:
            path: The repository path

        Returns:
            The git version
        """
        return ""

    def description(self) -> str | None:
        """Requests extraction of the project description"""
        return None

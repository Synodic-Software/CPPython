"""
TODO
"""

from pathlib import Path

from dulwich.porcelain import tag_list
from dulwich.repo import Repo
from packaging.version import Version

from cppython.console.vcs.base import VCS


class Git(VCS):
    """
    Git implementation hooks
    """

    def is_repository(self, path: Path) -> bool:
        """
        TODO
        """

        try:
            Repo(str(path))
            return True

        except Exception:
            return False

    def extract_version(self, path: Path) -> Version:
        """
        TODO
        """

        repo = Repo(str(path))
        tags = tag_list(repo)

        try:
            tag = tags[-1].decode("utf-8")
        except Exception:
            tag = "v0.1.0"
        return Version(tag)

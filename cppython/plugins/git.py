"""TODO
"""

from pathlib import Path

from cppython_core.schema import VersionControl
from dulwich.porcelain import tag_list
from dulwich.repo import Repo
from packaging.version import Version


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

        except Exception:
            return False

    def extract_version(self, path: Path) -> Version:
        """_summary_

        Args:
            path: _description_

        Returns:
            _description_
        """

        repo = Repo(str(path))
        tags = tag_list(repo)

        try:
            tag = tags[-1].decode("utf-8")
        except Exception:
            tag = "v0.1.0"
        return Version(tag)

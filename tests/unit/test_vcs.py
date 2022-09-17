"""TODO
"""


from pathlib import Path

from cppython.console.vcs.git import Git


class TestGit:
    """_summary_"""

    def test_version(self) -> None:
        """_summary_"""

        directory = Path()

        git = Git()

        result = git.extract_version(directory)

        assert result != ""

    def test_dulwich(self) -> None:
        """_summary_"""

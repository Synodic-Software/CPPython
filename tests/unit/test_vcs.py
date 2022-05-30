"""
TODO
"""


from pathlib import Path

from cppython.console.vcs.git import Git


class TestGit:
    """
    TODO
    """

    def test_version(self):
        """
        TODO
        """

        directory = Path()

        git = Git()

        result = git.extract_version(directory)

        assert result != ""

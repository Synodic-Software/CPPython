import pytest

from cppython.entry_points.console import cli
from click.testing import CliRunner
from pathlib import Path
from distutils.dir_util import copy_tree

# Fixtures
@pytest.fixture
def cli_workspace(test_workspace: Path) -> CliRunner:
    """
    @returns - A Test runner using the path to the temporary directory populated with a test workspace
    """

    runner = CliRunner()

    with runner.isolated_filesystem():
        target_path = Path.cwd()
        copy_tree(str(test_workspace), str(target_path))
        yield runner


class TestCLI:
    def test_validate(self, cli_workspace):
        result = cli_workspace.invoke(cli, ["validate"])

        if result.exception is not None:
            raise result.exception

    def test_install(self, cli_workspace):
        result = cli_workspace.invoke(cli, ["install"])

        if result.exception is not None:
            raise result.exception

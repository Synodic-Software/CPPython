import subprocess
import os

from click.testing import CliRunner
from cppoetry.console import cli


class TestWorkflow:
    def test_validation_workflow(self, tmp_workspace):
        runner = CliRunner()
        result = runner.invoke(cli, ["check"])

        assert result.exit_code == 0

    def test_development_workflow(self, tmp_workspace):

        environment = {
            **os.environ,
            "CONAN_USER_HOME": str(tmp_workspace / ".conan")
        }

        runner = CliRunner()

        result = runner.invoke(cli, ["install"])
        assert result.exit_code == 0

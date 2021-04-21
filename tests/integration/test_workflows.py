import subprocess
import os


class TestWorkflow:
    def test_validation(self, tmp_workspace):
        subprocess.run(["poetry", "check"], cwd=tmp_workspace, check=True)

    def test_development(self, tmp_workspace):

        environment = {
            **os.environ,
            "CONAN_USER_HOME": str(tmp_workspace / "conan_cache"),
            "POETRY_CACHE_DIR": str(tmp_workspace / "poetry_cache"),
            "POETRY_VIRTUALENVS_IN_PROJECT": "true",
        }

        subprocess.run(["poetry", "install"], cwd=tmp_workspace, check=True, env=environment)
        #subprocess.run(["poetry", "build"], cwd=tmp_workspace, check=True, env=environment)

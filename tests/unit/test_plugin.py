from synodic_poetry.plugin import SynodicPlugin
from conans.client.conan_api import ConanAPIV1


class TestFormat:
    def test_validation(self, tmp_workspace):
        with tmp_workspace:
            SynodicPlugin().poetry_check()

    def test_conan_exporting(self, tmp_workspace):
        with tmp_workspace:
            plugin = SynodicPlugin()
            ConanAPIV1().create(
                conanfile_path=plugin.data["tool"]["conan"]["install-path"],
                name=plugin.data["tool"]["poetry"]["name"],
                version=plugin.data["tool"]["poetry"]["version"],
                user=None,
                channel=None,
                profile_names=None,
                settings=None,
                options=None,
                env=None,
                test_folder=None,
                not_export=False,
                build_modes=None,
                keep_source=False,
                keep_build=False,
                verify=None,
                manifests=None,
                manifests_interactive=None,
                remote_name=None,
                update=False,
                cwd=None,
                test_build_folder=None,
                lockfile=None,
                ignore_dirty=False,
            )
